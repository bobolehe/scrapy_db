import datetime
import logging

import scrapy
from fortiguardPro.items import FortiguardproItem

from fortiguardPro import settings

logger = logging.getLogger(__name__)


class FortiguardSpider(scrapy.Spider):
    name = "fortiguard"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://www.fortiguard.com/encyclopedia?type=ips&page=1"]
    url = "https://www.fortiguard.com/encyclopedia?type=ips&page=%d"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.MYSQL_HOST = kwargs.get('host') if kwargs.get('host') else settings.MYSQL_HOST
        settings.MYSQL_USER = kwargs.get('user') if kwargs.get('user') else settings.MYSQL_USER
        settings.MYSQL_PWD = kwargs.get('pwd') if kwargs.get('pwd') else settings.MYSQL_PWD
        settings.MYSQL_PORT = kwargs.get('port') if kwargs.get('port') else settings.MYSQL_PORT
        settings.MYSQL_DB = kwargs.get('db') if kwargs.get('db') else settings.MYSQL_DB
        settings.MYSQL_TB = kwargs.get('tb') if kwargs.get('tb') else settings.MYSQL_TB
        self.page_max = int(kwargs.get('page')) if kwargs.get('page') else int(settings.PAGE_MAX)
        # 爬取页数
        self.page = 1

    def parse(self, response):
        logger.error(f'抓取当前url： {response.url}中文章url')
        # 爬取网页中文章
        div_list = response.xpath('//*[@id="two-column"]/div[2]/div[2]/section/div[2]/div')

        for div in div_list:
            try:
                # 文章名称
                data_name = div.xpath('./div/div[1]/a/text()').extract_first()
                # 文章发布日期
                data_time = div.xpath('./div/div[3]//span[1]/text()').extract_first().strip()
                # 文章链接
                data_url = "https://www.fortiguard.com" + div.xpath('./div/div[1]/a/@href').extract_first()
            except:
                # 页面数据获取失败重新获取数据
                yield scrapy.Request(url=response.url, callback=self.parse)
            else:
                data_time = self.datestime(stime=data_time)
                item = FortiguardproItem()
                item['rule_name'] = data_name
                item['rule_time'] = data_time
                item['url'] = data_url
                self.data_max += 1
                yield scrapy.Request(url=data_url, callback=self.parse_url, meta={"item": item}, dont_filter=True)

        self.page += 1
        if self.page <= self.page_max:
            url = format(self.url % self.page)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse_url(self, response):
        try:
            item = response.meta['item']
            # xpath解析页面数据
            div = response.xpath('//*[@id="two-column"]')
            id = div.xpath('./div[1]/div/div[2]/table//tr[1]/td[2]/text()').extract_first()
            Updated = div.xpath('./div[1]/div/div[2]/table//tr[3]/td[2]/text()').extract_first()
            UpdatedStime = self.datestime(Updated)
            title = div.xpath('./div[2]/div[2]/section/div[1]/h2/text()').extract_first()
            # Recommended Actions字段下全部内容进行拼接，并将引号进行格式化
            actions_list = div.xpath('./div[2]/div[2]/section/div[5]/p//text()').extract()
            Recommend_actions = ' '.join(actions_list)
            Recommend_actions = Recommend_actions.replace('"', '\\"')
            CVE_References = div.xpath('./div[2]/div[2]/section/div[6]/a/text()').extract_first()
            Other_References = div.xpath('./div[2]/div[2]/section/div[7]/a/text()').extract_first()
            # 传递item对象中
            item['UpdatedStime'] = UpdatedStime
            item['rule_id'] = id
            item['rule_title'] = title
            item['Recommend_actions'] = Recommend_actions
            item['CVE_References'] = CVE_References
            item['Other_References'] = Other_References
            item['stime'] = str(datetime.datetime.now())

            # 判断部分标签内容是否存在
            if id and CVE_References:
                logger.error(f'文章详情页：{response.url},数据缓存成功')
            elif not id:
                logger.error(f'{response.url},id参数抓取失败重新爬取')
                yield scrapy.Request(url=item['url'], callback=self.parse_url, meta={'item': item})
            elif not CVE_References:
                self.max += 1
                logger.error(f'文章详情页：{response.url},详情页缺少CVE参数无需实例化')
                return
            print(item)
            # 数据库校验数据进行下一步操作
            data = self.data
            ye = self.VerificationData(Mdata=data, item=item, response=response)
            if ye:
                logger.error(f"进行实例化{item['url']}地址数据")
                yield item
            else:
                logger.error(f"{item['url']}数据已是最新内容，无需实例化")

        except Exception as e:
            logger.error(f'详情页：{response.url},数据处理失败：{e}')

    def datestime(self, stime):
        date = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
        }

        stime = stime
        stime = stime.replace(',', '').split(' ')

        stime[0] = str(date[stime[0]])
        stime = [stime[2], stime[0], stime[1]]
        return '-'.join(stime)

    def VerificationData(self, Mdata, item, response):
        """

        :param self:
        :param Mdata:
        :param item:
        :param response:
        :return:
        """
        try:
            # 校验数据是否存在数据库
            err = Mdata.price_exists(field="rule_id", price=item['rule_id'])
            # 不存在数据库，直接进行存储
            if err['error'] == 101:
                item['datamax'] = 1
                return item
            # 查询语句出错，返回信息，停止程序
            elif err['error'] == 104 or err['error'] == 103:
                logger.error(f'{item["url"]}数据查询失败：错误信息{err["log"]}')
                self.crawler.engine.close_spider(self, '数据库查询信息出错')

            # 查询数据库中已有数据的数据更新时间
            data_stime = Mdata.query_page(field=item['rule_id'], name='UpdatedStime', fields='rule_id')[0]
            # 没有数据更新时间，再次进行存储
            if not data_stime:
                logger.error(f'{item["url"]}数据存在,但无更新日期，进行更新')
                item['datamax'] = Mdata.query_page(field=item['rule_id'], name='datamax', fields='rule_id')[0]
                item['datamax'] = int(item['datamax']) + 1 if item['datamax'] else 1

                return item
            # 存在更新时间与当前爬取到时间比较，是否需要数据存储
            date_obj = datetime.datetime.strptime(item['UpdatedStime'], "%Y-%m-%d")
            # 有新的更新时间进行数据存储
            if data_stime < date_obj:
                logger.error(f'更新{item["url"]}数据')
                item['datamax'] = Mdata.query_page(field=item['rule_id'], name='datamax', fields='rule_id')[0]
                item['datamax'] = int(item['datamax']) + 1 if item['datamax'] else 1
                return item
            # 无须存储
            logger.error(f'{item["url"]}数据存在，更新日期为最新，无需更新')
        except Exception as e:
            logger.error(f"数据库校验数据失败，错误信息{e}")
