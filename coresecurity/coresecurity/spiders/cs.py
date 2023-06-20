import scrapy
import datetime
import logging
from coresecurity.items import CoresecurityItem
from coresecurity import settings
from coresecurity.id_tool.id_seq import IdSeq
from coresecurity.id_tool.id_generator import IdGenerator

# 实例化日志类
logger = logging.getLogger(__name__)


class CsSpider(scrapy.Spider):
    name = "cs"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://www.coresecurity.com/core-labs/exploits?page=0"]
    url = "https://www.coresecurity.com/core-labs/exploits?page=%d"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.MYSQL_HOST = kwargs.get('host') if kwargs.get('host') else settings.MYSQL_HOST
        settings.MYSQL_USER = kwargs.get('user') if kwargs.get('user') else settings.MYSQL_USER
        settings.MYSQL_PWD = kwargs.get('pwd') if kwargs.get('pwd') else settings.MYSQL_PWD
        settings.MYSQL_PORT = kwargs.get('port') if kwargs.get('port') else settings.MYSQL_PORT
        settings.MYSQL_DB = kwargs.get('db') if kwargs.get('db') else settings.MYSQL_DB
        settings.MYSQL_TB = kwargs.get('tb') if kwargs.get('tb') else settings.MYSQL_TB
        self.page_max = int(kwargs.get('page')) if kwargs.get('page') else int(0)
        self.page = int(0)
        self.new_data = int(0)

    def parse(self, response):
        # .extract_first()
        if self.new_data >= 25:
            self.crawler.engine.close_spider(self, "重复数据达到最大限制，结束爬取")
        # 如果没有传递指定页数，自动获取最终页数
        if not self.page_max:
            page = response.xpath(
                '//*[@id="block-views-block-exploits-block-1"]/div/div/div/nav/ul/li[@class="pager__item--next"]/following-sibling::*[1]/a/@href').extract_first()
            self.page_max = int(page.split('=')[-1])
        # 获取此页表格每一行
        tr_list = response.xpath(
            '//*[@id="main"]//main//div[@class="content"]//div[@class="view-content row"]//tbody/tr')

        self.new_data = 0
        # 遍历表格每一行
        for tr in tr_list:
            item = CoresecurityItem()
            # 获取一次id
            ID = IdGenerator(IdSeq.coresecurity.value)
            # 解析 每行，每列内容
            title = ''.join(
                tr.xpath('./td[@class="word-wrap views-field views-field-title"]//text()').extract()).strip()
            description = ''.join(
                tr.xpath('./td[@class="word-wrap views-field views-field-body"]//text()').extract()).strip()
            date_added = ''.join(tr.xpath('./td[@class="views-field views-field-created"]//text()').extract()).strip()
            CVE = ''.join(tr.xpath('./td[@class="views-field views-field-field-cve-link"]/a//text()').extract()).strip()
            Platform = ''.join(tr.xpath(
                './td[@class="views-field views-field-field-exploit-platform"]//text()').extract()).strip()
            Exploit_type = ''.join(tr.xpath(
                './td[@class="views-field views-field-field-exploit-type"]//text()').extract()).strip()
            product = ''.join(
                tr.xpath('./td[@class="views-field views-field-field-product-name"]//text()').extract()).strip()
            # 向item对象传值
            url = 'https://www.coresecurity.com/core-labs/exploits?exploit_name=' + '+'.join(title.split(' '))
            item['id'] = ID.get_id()
            item['url'] = url
            item['title'] = title
            item['Description'] = description
            item['vulnerabilty'] = CVE
            item['category'] = Exploit_type
            item['platform'] = Platform
            item['update_time'] = self.datestime(date_added)
            item['stime'] = str(datetime.datetime.now())
            # 数据总数加1
            self.data_max += 1
            # 导入存储在类中的数据库类 查询是否在数据库中存在
            data = self.data
            err = self.VerificationData(Mdata=data, item=item, response=response)
            if not err:
                logger.error(f"{item['url']}数据已是最新内容，无需实例化")
                self.new_data += 1
                continue
            yield item

        self.page += 1
        if self.page < self.page_max:
            url = format(self.url % self.page)
            yield scrapy.Request(url=url, callback=self.parse)

    def datestime(self, stime):

        """
        简单翻译爬取到的英语月份
        :param self:
        :param stime:
        :return:
        """
        date1 = {
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
        date2 = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }

        stime = stime
        stime = stime.replace(',', '').split(' ')

        stime[0] = str(date2[stime[0]])
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
            err = Mdata.price_exists(field='title', price=item['title'])
            # 不存在数据库，直接进行存储
            if err['error'] == 101:
                item['datamax'] = 1
                return item
            # 查询语句出错，返回信息，停止程序
            elif err['error'] == 104 or err['error'] == 103:
                logger.error(f'{item["url"]}数据查询失败：错误信息{err["log"]}')
                self.crawler.engine.close_spider(self, '数据库查询信息出错')

            # 查询数据库中已有数据的数据更新时间
            data_stime = Mdata.query_page(field=item['title'], name='update_time', fields='title')[0]
            # 没有数据更新时间，再次进行存储
            if not data_stime:
                logger.error(f'{item["url"]}数据存在,但无更新日期，进行更新')
                item['datamax'] = int(
                    Mdata.query_page(field=item['title'], name='datamax', fields='title')[0]) + 1
                return item
            # 存在更新时间与当前爬取到时间比较，是否需要数据存储
            date_obj = datetime.datetime.strptime(item['update_time'], "%Y-%m-%d")
            # 有新的更新时间进行数据存储
            if data_stime < date_obj:
                logger.error(f'更新{item["url"]}数据')
                item['datamax'] = int(
                    Mdata.query_page(field=item['title'], name='datamax', fields='title')[0]) + 1
                return item

        except Exception as e:
            logger.error(f"数据库校验数据失败，错误信息{e}")
