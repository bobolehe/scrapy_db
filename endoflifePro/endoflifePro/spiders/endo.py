import scrapy
import re
import json
import datetime
from endoflifePro.items import EndoflifeproItem
from endoflifePro import settings
import logging

# 实例化日志类
logger = logging.getLogger(__name__)


class EndoSpider(scrapy.Spider):
    name = "endo"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://endoflife.date/api/all.json"]
    url_home = "https://endoflife.date/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.MYSQL_HOST = kwargs.get('host') if kwargs.get('host') else settings.MYSQL_HOST
        settings.MYSQL_USER = kwargs.get('user') if kwargs.get('user') else settings.MYSQL_USER
        settings.MYSQL_PWD = kwargs.get('pwd') if kwargs.get('pwd') else settings.MYSQL_PWD
        settings.MYSQL_PORT = kwargs.get('port') if kwargs.get('port') else settings.MYSQL_PORT
        settings.MYSQL_DB = kwargs.get('db') if kwargs.get('db') else settings.MYSQL_DB
        settings.MYSQL_TB = kwargs.get('tb') if kwargs.get('tb') else settings.MYSQL_TB
        self.page_max = kwargs.get('page') if kwargs.get('page') else 10

    def parse(self, response):
        # print(len(response.json()))
        for i in response.json():
            url = self.url_home + i
            self.data_max += 1
            yield scrapy.Request(url=url, callback=self.data_parse)

    def data_parse(self, response):
        item = EndoflifeproItem()
        logger.error(f"爬取详情页链接{response.url}")
        datatime = response.xpath('//*[@id="main-content"]/div[@class="product-title"]/time/@datetime').extract_first()

        item['datatime'] = datatime

        item["title"] = response.xpath(
            '//*[@id="main-content"]/div[@class="product-title"]/div//h1/text()').extract_first().replace('\n',
                                                                                                          '').strip()
        item["url"] = response.url

        # 导入存储在类中的数据库类 查询是否在数据库中存在
        data = self.data
        err = self.VerificationData(Mdata=data, item=item, response=response)
        if not err:
            logger.error(f"{response.url}数据已是最新内容，无需实例化")
            return

        th_list = response.xpath('//*[@id="main-content"]/div[@class="table-wrapper"]//thead//th/text()').extract()
        item["table_title"] = th_list
        tr_list = response.xpath('//*[@id="main-content"]/div[@class="table-wrapper"]//thead/following-sibling::tr')
        tr_data = []
        for tr in tr_list:
            clas = tr.xpath('./@class').extract_first()
            if not (clas == "d-none"):
                data_list = tr.xpath('./td')
                trr_data = []

                for data in data_list:
                    d = "".join(data.xpath('.//text()').extract()).replace('\n', '').strip()
                    # print(''.join(data.xpath('.//text()').extract()).replace('\n', '').strip())
                    trr_data.append(d)
                trr_data = trr_data

                i = 0
                trr_json = {}
                while i < len(th_list):
                    trr_json[th_list[i]] = trr_data[i]
                    i += 1
                tr_data.append(trr_json)

        item["table_data"] = tr_data
        item['version'] = "".join(response.xpath('//*[@id="version-command"]//text()').extract()).replace('\n',
                                                                                                          '').strip()
        logger.error(f"{response.url}数据缓存成功")
        item['stime'] = str(datetime.datetime.now())
        item['title'] = item['title']
        item['table_title'] = item['table_title']
        item['table_data'] = item['table_data']
        item['version'] = item['version']
        yield item

    def VerificationData(self, Mdata, item, response):
        try:
            # 校验数据是否存在数据库
            err = Mdata.price_exists(field='url', price=item['url'])
            # 不存在数据库，直接进行存储
            if err['error'] == 101:
                item['pagemax'] = 1
                return item
            # 查询语句出错，返回信息，停止程序
            elif err['error'] == 104 or err['error'] == 103:
                logger.error(f'{response.url}数据查询失败：错误信息{err["log"]}')
                self.crawler.engine.close_spider(self, '数据库查询信息出错')

            # 查询数据库中已有数据的数据更新时间
            data_stime = Mdata.query_page(field=item['url'], name='datatime', fields='url')[0]
            data_stime = data_stime.astimezone() if data_stime else data_stime
            # 没有数据更新时间，再次进行存储
            if not data_stime:
                logger.error(f'{response.url}数据存在,但无更新日期，进行更新')
                item['pagemax'] = int(Mdata.query_page(field=item['url'], name='pagemax', fields='url')[0]) + 1
                return item
            # 存在更新时间与当前爬取到时间比较，是否需要数据存储
            date_obj = datetime.datetime.strptime(item['datatime'], "%Y-%m-%dT%H:%M:%S%z").astimezone()
            # 有新的更新时间进行数据存储
            if data_stime < date_obj:
                item['pagemax'] = int(Mdata.query_page(field=item['url'], name='pagemax', fields='url')[0]) + 1
                return item

        except Exception as e:
            logger.error(f"数据库校验数据失败，错误信息{e}")
