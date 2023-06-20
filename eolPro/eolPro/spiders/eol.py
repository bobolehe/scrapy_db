import json
import re
import scrapy
import datetime
from eolPro.items import EolproItem
from eolPro import settings
import logging

# 实例化日志类
logger = logging.getLogger(__name__)


class EolSpider(scrapy.Spider):
    name = "eol"
    start_urls = ["https://serviceexpress.com/resources/eol-eosl-database/?start=-90&timespan=90"]
    url_list = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.MYSQL_HOST = kwargs.get('host') if kwargs.get('host') else settings.MYSQL_HOST
        settings.MYSQL_USER = kwargs.get('user') if kwargs.get('user') else settings.MYSQL_USER
        settings.MYSQL_PWD = kwargs.get('pwd') if kwargs.get('pwd') else settings.MYSQL_PWD
        settings.MYSQL_PORT = kwargs.get('port') if kwargs.get('port') else settings.MYSQL_PORT
        settings.MYSQL_DB = kwargs.get('db') if kwargs.get('db') else settings.MYSQL_DB
        settings.MYSQL_TB = kwargs.get('tb') if kwargs.get('tb') else settings.MYSQL_TB
        self.page_max = int(kwargs.get('page')) if kwargs.get('page') else int(0)
        # 数据页分页中最大页数
        self.product_page_max = {}
        # 指定爬取页数
        self.spider_page_max = {}
        # 数据爬取时不同的url
        self.product_url = {}
        # 数据库中最大页数
        self.data_page_max = {}
        # 当前爬取数据页数
        self.page = {}

    def parse(self, response):
        button_list = response.xpath(
            '//*[@id="main"]//div[@class="page-default"]/article/div/div/div[2]/div/div[2]/div[2]/div/button')
        for button in button_list:
            url = button.xpath('./following-sibling::div[1]/p/a/@href').extract_first()
            self.url_list.append(url)
            product = url.split('/')[6]
            # 获取数据库中数据是否存在上次爬取时存储最大页数
            data = self.data
            err = data.query_page(field=product, page='PageMax', fields='product')
            pattern = r'^-?\d+(\.\d+)?$'
            if err:
              if re.match(pattern, err):
                  self.data_page_max[product] = int(err)
              else:
                  self.data_page_max[product] = 0
            else:
              self.data_page_max[product] = 0

            # 分别存储 不同的页数最大值和url地址，在爬取分页页面时使用
            # 初始化爬取开始页数
            self.page[product] = 1
            # 如果有指定爬取页数
            if self.page_max:
                self.spider_page_max[product] = self.page_max
            # 初始化一个不同url分组字典
            self.product_page_max[product] = 0
            # 将不同项目url初始化到字典中
            self.product_url[product] = f'https://serviceexpress.com/resources/eol-eosl-database/oem/{product}/'

        for url in self.url_list:
            yield scrapy.Request(url=url, callback=self.datapage)

    def datapage(self, response):
        logger.error(f"爬取分页链接{response.url}")
        # 获取到分页页面中所有详情页的url
        cisco_list = response.xpath(
            '//*[@id="main"]/div[@class="archive-content"]/div/section/div/table//tr/td/a/@href').extract()
        # 从url中取出url归属于哪一个项目分类
        product = response.url.split('/')[6]

        # 判断此项目中最大页数是否有保存，没有则获取页面中最大页数
        if not self.product_page_max[product]:
            self.product_page_max[product] = int(response.xpath(
                '//*[@id="main"]/div[2]/div/section/nav/div/span[2]/span/text()').extract_first())

        # 遍历出分页链接中的详情页url地址
        for url in cisco_list:
            item = EolproItem()
            item['url'] = url
            item['product'] = json.dumps(product)
            item['PageMax'] = json.dumps(self.product_page_max[product])
            item['dataPage'] = json.dumps(self.page[product])

            # 导入存储在类中的数据库类 查询是否在数据库中存在
            data = self.data
            self.data_max += 1
            # 校验此条数据是否存在数据库
            err = data.price_exists(field='url', price=url)

            # 不存在数据库，进行详情页的爬取
            if err['error'] == 101:
                logger.error(f"跳转详情页进行爬取{url}")
                yield scrapy.Request(url=url, callback=self.DataSpider, meta={"item": item})
            else:
                logger.error(err['log'])

        # 判断页数是否有指定，否则自动获取全部页数，作为爬取目标
        if self.spider_page_max:
            # 避免部分分页页数数量有限
            if self.spider_page_max[product] > self.product_page_max[product]:
                self.spider_page_max[product] = self.product_page_max[product]

            self.page[product] += 1
            if self.page[product] <= self.spider_page_max[product]:
                url = self.product_url[product] + f'page/{self.page[product]}/'
                yield scrapy.Request(url=url, callback=self.datapage)
        # 没有指定爬取页数，那么会获取全部数据，数据库存在部分数据情况下，
        else:
            self.page[product] += 1
            # 这里如果有获取到存在数据，数据页有固定页数情况，使用+1操作保障数据溢出
            if self.data_page_max[product]:
                if self.page[product] <= self.product_page_max[product] - self.data_page_max[product]:
                    url = self.product_url[product] + f'page/{self.page[product]}/'
                    yield scrapy.Request(url=url, callback=self.datapage)
            else:
                if self.page[product] <= self.product_page_max[product]:
                    url = self.product_url[product] + f'page/{self.page[product]}/'
                    yield scrapy.Request(url=url, callback=self.datapage)

    def DataSpider(self, response):
        # 详情页爬取方法
        try:
            logger.error(f"爬取详情页{response.url}数据")
            item = response.meta['item']
            title = response.xpath(
                '//*[@id="single-eol-database-heading"]/text()').extract_first()
            # 部分页面数据不存在，进行跳过
            if not title:
                raise Exception('页面数据不存在')
            # 页面正常，进行数据提取
            item['title'] = json.dumps(title)
            data_list = response.xpath(
                '//*[@id="main"]/div[@class="page-single-eol-database"]/article//div[@class="single-eol-database__meta-item"]')

            for data in data_list:
                dt = data.xpath('./dt/h2/text()').extract()
                dd = data.xpath('./dd//text()').extract()
                dt = "".join(dt).strip().replace(" ", "")[0:4]
                dd = "".join(dd).strip()
                item[dt] = json.dumps(dd)
            item['stime'] = str(datetime.datetime.now())
            # 返回item对象进行数据库实例化存储
            yield item
        except:
            self.max += 1
            logger.error(f"详情页{response.url}无数据")
