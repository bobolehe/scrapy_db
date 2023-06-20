import datetime
import time
import logging

import scrapy
from cxsecurity.id_tool.id_generator import IdGenerator
from cxsecurity.id_tool.id_seq import IdSeq
from cxsecurity.items import CxsecurityItem

from cxsecurity import settings

# 实例化日志类
logger = logging.getLogger(__name__)


class CxseSpider(scrapy.Spider):
    name = "cxse"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://cxsecurity.com/exploit/1"]
    # start_urls = ["https://cxsecurity.com/issue/WLB-2023050027"]
    url = "https://cxsecurity.com/exploit/%d"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.MYSQL_HOST = kwargs.get('host') if kwargs.get('host') else settings.MYSQL_HOST
        settings.MYSQL_USER = kwargs.get('user') if kwargs.get('user') else settings.MYSQL_USER
        settings.MYSQL_PWD = kwargs.get('pwd') if kwargs.get('pwd') else settings.MYSQL_PWD
        settings.MYSQL_PORT = kwargs.get('port') if kwargs.get('port') else settings.MYSQL_PORT
        settings.MYSQL_DB = kwargs.get('db') if kwargs.get('db') else settings.MYSQL_DB
        settings.MYSQL_TB = kwargs.get('tb') if kwargs.get('tb') else settings.MYSQL_TB
        self.page_setting = int(kwargs.get('page')) if kwargs.get('page') else int(0)
        self.page_max = 1
        self.page = 1
        self.data_list = list()

    def parse(self, response):
        if response.status != 200:
            yield scrapy.Request(url=response.url, callback=self.parse, meta={'download_timeout': 10}, dont_filter=True)
            return
        # .extract_first()
        # print(response.text)
        # print(response.url)
        a_list = response.xpath('//*[@id="general"]/table//tr//td//div[@class="col-md-7"]//a')
        for i, a in enumerate(a_list):
            item = CxsecurityItem()
            url = a.xpath('./@href').extract_first()
            title = a.xpath('./@title').extract_first()
            item['url'] = url
            item['title'] = title

            page_max = str(response.xpath(
                '//*[@id="general"]//td[@id="glowna"]//script[@type="text/javascript"][2]//text()').extract_first())
            if not page_max:
                yield scrapy.Request(url=response.url, callback=self.parse, meta={'download_timeout': 10},
                                     dont_filter=True)
            page_max = int(page_max.split(';')[1].split(" = ")[1]) + 1

            requests = scrapy.Request(url=item['url'],
                                      meta={'item': item, 'download_timeout': 10, 'data_page': i, 'page': page_max},
                                      callback=self.data_spider, dont_filter=True)
            yield requests

    def data_spider(self, response):
        item = response.meta['item']
        data_page = response.meta['data_page']
        page = response.meta['page']
        if response.status != 200:
            yield scrapy.Request(url=response.url, callback=self.data_spider,
                                 meta={'item': item, 'download_timeout': 10, 'data_page': data_page, 'page': page},
                                 dont_filter=True)
            return
        try:
            # 详情页抓取
            published = response.xpath(
                '//*[@id="general"]//td[@id="glowna"]//table//div[@class="container"]/div[@class="row"]/div[@class="col-xs-12 col-md-3"]//b/text()').extract_first()
            risk = response.xpath(
                '//*[@id="general"]//td[@id="glowna"]//table//div[@class="container"]/div[@class="row"]/div[@class="col-xs-5 col-md-3"]//span//text()').extract_first()
            local = response.xpath(
                '//*[@id="general"]//td[@id="glowna"]//table//div[@class="container"]/div[@class="row"]/div[@class="col-xs-3 col-md-3"]//b//text()').extract_first()
            remote = response.xpath(
                '//*[@id="general"]//td[@id="glowna"]//table//div[@class="container"]/div[@class="row"]/div[@class="col-xs-4 col-md-3"]//b//text()').extract_first()
            cve = response.xpath(
                '//*[@id="general"]//td[@id="glowna"]//table//div[@class="container"]/div[@class="row"]/div[@class="col-xs-6 col-md-3"][1]//b//text()').extract_first()
            cwe = response.xpath(
                '//*[@id="general"]//td[@id="glowna"]//table//div[@class="container"]/div[@class="row"]/div[@class="col-xs-6 col-md-3"][2]//b//text()').extract_first()

            # 获取一次id
            ID = IdGenerator(IdSeq.coresecurity.value)
            item['id'] = ID.get_id()
            item['published_time'] = published
            if published:
                if '/' in published:
                    item['published_time'] = published.split(' / ')[0]
                else:
                    item['published_time'] = '-'.join(published.split('.'))
            item['risk'] = risk
            item['local'] = local
            item['remote'] = remote
            item['cve'] = cve
            item['cwe'] = cwe
            item['stime'] = str(datetime.datetime.now())
        except Exception as e:
            logger.error(f"获取详情页{response.url}数据失败，错误信息{e}")
        else:
            # 数据总数加1
            self.data_max += 1
            # 导入存储在类中的数据库类 查询是否在数据库中存在
            data = self.data
            err = self.VerificationData(Mdata=data, item=item, response=response)
            if not err:
                logger.error(f"{item['url']}数据已是最新内容，无需实例化")
            else:
                yield item

            if data_page == 59:
                if self.page_setting:
                    self.page += 1
                    if self.page <= self.page_setting:
                        url = format(self.url % self.page)
                        yield scrapy.Request(url=url, callback=self.parse, meta={'download_timeout': 10},
                                             dont_filter=True)
                else:
                    self.page += 1
                    if self.page == page:
                        url = format(self.url % self.page)
                        yield scrapy.Request(url=url, callback=self.parse, meta={'download_timeout': 10},
                                             dont_filter=True)

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
            err = Mdata.price_exists(field='url', price=item['url'])
            # 不存在数据库，直接进行存储
            if err['error'] == 101:
                item['datamax'] = 1
                return item
            # 查询语句出错，返回信息，停止程序
            elif err['error'] == 104 or err['error'] == 103:
                logger.error(f'{item["url"]}数据查询失败：错误信息{err["log"]}')
                self.crawler.engine.close_spider(self, '数据库查询信息出错')

            # 查询数据库中已有数据的数据更新时间
            data_stime = Mdata.query_page(field=item['url'], name='published_time', fields='url')[0]
            # 没有数据更新时间，再次进行存储
            if not data_stime:
                logger.error(f'{item["url"]}数据存在,但无更新日期，进行更新')
                item['datamax'] = int(
                    Mdata.query_page(field=item['url'], name='datamax', fields='url')[0]) + 1
                return item
            # 存在更新时间与当前爬取到时间比较，是否需要数据存储
            date_obj = datetime.datetime.strptime(item['published_time'], "%Y-%m-%d")
            # 有新的更新时间进行数据存储
            if data_stime < date_obj:
                logger.error(f'更新{item["url"]}数据')
                item['datamax'] = int(
                    Mdata.query_page(field=item['url'], name='datamax', fields='url')[0]) + 1
                return item

        except Exception as e:
            logger.error(f"数据库校验数据失败，错误信息{e}{item['url']}")
