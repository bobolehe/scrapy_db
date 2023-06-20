import json

import scrapy
import datetime
from kbPro.items import KbproItem
import logging
from kbPro import settings

logger = logging.getLogger(__name__)


class KbSpider(scrapy.Spider):
    name = "kb"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://www.kb.cert.org/vuls/bypublished/desc/?page=1"]
    url = "https://www.kb.cert.org/vuls/bypublished/desc/?page=%d"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.MYSQL_HOST = kwargs.get('host') if kwargs.get('host') else settings.MYSQL_HOST
        settings.MYSQL_USER = kwargs.get('user') if kwargs.get('user') else settings.MYSQL_USER
        settings.MYSQL_PWD = kwargs.get('pwd') if kwargs.get('pwd') else settings.MYSQL_PWD
        settings.MYSQL_PORT = kwargs.get('port') if kwargs.get('port') else settings.MYSQL_PORT
        settings.MYSQL_DB = kwargs.get('db') if kwargs.get('db') else settings.MYSQL_DB
        settings.MYSQL_TB = kwargs.get('tb') if kwargs.get('tb') else settings.MYSQL_TB
        self.page_max = int(kwargs.get('page')) if kwargs.get('page') else int(0)
        self.page = 1

    def parse(self, response):
        tr_list = response.xpath('//*[@id="content"]/div/div/table/tbody/tr')
        logger.error(f'抓取当前url： {response.url}文章url，当前文章列表页文章数量 {len(tr_list)}')

        for tr in tr_list:
            item = KbproItem()
            item['Updated_time'] = tr.xpath('.//td[3]/text()').extract_first().strip()
            item['CCid'] = tr.xpath('.//td[4]/text()').extract_first().strip()
            td_url = tr.xpath('.//td[6]/a/@href').extract_first()
            url = 'https://www.kb.cert.org' + td_url

            # 导入存储在类中的数据库类 查询是否在数据库中存在
            data = self.data
            self.data_max += 1
            # 校验此条数据是否存在数据库
            err = data.price_exists(field='CCid', price=item['CCid'])

            if err['error'] == 101:
                logger.error(f"跳转详情页进行爬取{url}")
                item['PageMax'] = 1
                yield scrapy.Request(url=url, callback=self.home, meta={"item": item}, dont_filter=True)
            # 查询语句出错，返回信息，停止程序
            elif err['error'] == 104 or err['error'] == 103:
                logger.error(f'{response.url}数据查询失败：错误信息{err["log"]}')
                self.crawler.engine.close_spider(self, '数据库查询信息出错')
            else:
                # 存在更新时间与当前爬取到时间比较，是否需要数据存储
                data_stime = data.query_page(field=item['CCid'], name='Updated_time', fields='CCid')[0]
                date_obj = datetime.datetime.strptime(item['Updated_time'], "%Y-%m-%d")
                # 有新的更新时间进行数据存储
                if data_stime < date_obj:
                    logger.error(f"详情页{url}数据有更新，跳转爬取")
                    item['PageMax'] = int(data.query_page(field=item['CCid'], name='PageMax', fields='CCid')[0]) + 1
                    yield scrapy.Request(url=url, callback=self.home, meta={"item": item}, dont_filter=True)
                logger.error(f"详情页{url}数据已存在，无需更新")

        # 判断是否有传递指定爬取页数，没有指定则获取最大页数
        if not self.page_max:
            response_page = response.xpath(
                '//*[@id="content"]/div/div/ul/li[last()]/preceding-sibling::*[1]//text()').extract_first()
            self.page_max = int(response_page)

        self.page += 1
        if self.page <= self.page_max:
            url = format(self.url % self.page)
            yield scrapy.Request(url=url, callback=self.parse)

    def home(self, response):
        url = response.url
        logger.error(f'爬取文章详情页： {url}')
        try:
            item = response.meta['item']
            item['url'] = url
            title = response.xpath(
                '//*[@id="wrapper"]/div[@class="mainbody section"]/div[@class="row"]//h2[@class="subtitle"]/text()').extract_first()
            item['title'] = title

            # 获取正文中内容
            blog_post = response.xpath(
                '//*[@id="content"]/div[1]/div/div[1]/div/child::*')
            suoyin = [0]
            overviews = []
            descriptions = []
            impacts = []
            solutions = []
            for b, i in enumerate(blog_post):
                if i.xpath('./@id').extract_first() == "description":
                    overviews = blog_post[suoyin[-1] + 1:b]
                    suoyin.append(b)
                elif i.xpath('./@id').extract_first() == "impact":
                    descriptions = blog_post[suoyin[-1] + 1:b]
                    suoyin.append(b)
                elif i.xpath('./@id').extract_first() == "solution":
                    impacts = blog_post[suoyin[-1] + 1:b]
                    suoyin.append(b)
                elif i.xpath('./@id').extract_first() == "acknowledgements":
                    solutions = blog_post[suoyin[-1] + 1:b]
                    suoyin.append(b)
                elif i.xpath('./@id').extract_first() == "vendor-information" and not solutions:
                    solutions = blog_post[suoyin[-1] + 1:b]
                    suoyin.append(b)

            Overview = ""
            for text in overviews:
                for i in text.xpath(".//text()").extract():
                    Overview += i.strip()
            Description = ""
            for text in descriptions:
                for i in text.xpath(".//text()").extract():
                    Description += i.strip()
            Impact = ""
            for text in impacts:
                for i in text.xpath(".//text()").extract():
                    Impact += i.strip()
            Solution = ""
            for text in solutions:
                for i in text.xpath(".//text()").extract():
                    Solution += i.strip()

            # 获取References
            references = response.xpath(
                '//*[@id="content"]//div[@class="blog-post"]//a[@class="vulreflink"]/@href').extract()
            item['Referenc'] = json.dumps(''.join(references))

            # Other Information
            tr_list = response.xpath(
                '//*[@id="content"]/div/div[@class="blog-post"]/div/table[@class="unstriped"]/tbody/tr')
            other_data = {}
            for tr in tr_list:
                td1 = tr.xpath('./td[1]//text()').extract()
                td1 = "".join(td1).strip().replace(':', "")
                td2 = tr.xpath('./td[2]//text()').extract()
                key = []
                for td in td2:
                    td = td.strip()
                    if td:
                        key.append(td.strip())
                other_data[td1] = key

            # 爬取到内容传递至item对象字典中
            item["Overview"] = json.dumps(Overview)
            item["Description"] = json.dumps(Description)
            item["Impact"] = json.dumps(Impact)
            item["Solution"] = json.dumps(Solution)
            item['OtherInformation'] = json.dumps(other_data)
            item['stime'] = str(datetime.datetime.now())
            yield item
        except:
            logger.error(f'文章详情页:{url}爬取数据失败')
