import scrapy
import json

import datetime
from snykcrawler.items import SnykcrawlerItem
from snykcrawler import settings
import logging
# 实例化日志类
logger = logging.getLogger(__name__)


class SnykSpider(scrapy.Spider):
    name = "snyk"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://security.snyk.io/vuln"]
    url = "https://security.snyk.io/vuln/%d"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.MYSQL_HOST = kwargs.get('host') if kwargs.get('host') else settings.MYSQL_HOST
        settings.MYSQL_USER = kwargs.get('user') if kwargs.get('user') else settings.MYSQL_USER
        settings.MYSQL_PWD = kwargs.get('pwd') if kwargs.get('pwd') else settings.MYSQL_PWD
        settings.MYSQL_PORT = kwargs.get('port') if kwargs.get('port') else settings.MYSQL_PORT
        settings.MYSQL_DB = kwargs.get('db') if kwargs.get('db') else settings.MYSQL_DB
        settings.MYSQL_TB = kwargs.get('tb') if kwargs.get('tb') else settings.MYSQL_TB
        self.page_max = int(kwargs.get('page')) if kwargs.get('page') else settings.PAGE_MAX
        if self.page_max > settings.PAGE_MAX:
            self.page_max = settings.PAGE_MAX
        self.page = 1
        self.repeat_num = 0

    def parse(self, response):
        logger.error(f'抓取分页数据，分页url：{response.url}')
        tr_list = response.xpath('//*[@id="sortable-table"]/tbody/tr')

        for tr in tr_list:
            item = SnykcrawlerItem()
            # .extract_first()
            item['Vulnerability'] = tr.xpath('./td[1]/a/text()').extract_first().strip()
            item['url'] = tr.xpath('./td[1]/a/@href').extract_first().strip()
            item['stime'] = str(datetime.datetime.now())
            if tr.xpath('./td[2]/a'):
                item['Affecting'] = f"影响{tr.xpath('./td[2]/a/text()').extract_first().strip()}软件包"
                item['second_url'] = tr.xpath('./td[2]/a/@href').extract_first().strip()
                item['Version'] = f"影响版本：{tr.xpath('./td[2]/span/text()').extract_first().strip()}"
            else:
                item['Affecting'] = f"影响{tr.xpath('./td[2]/span[1]/text()').extract_first().strip()}软件包"
                item['Version'] = f"影响版本：{tr.xpath('./td[2]/span[2]/text()').extract_first().strip()}"

            item['Type'] = tr.xpath('./td[3]/span/text()').extract_first().strip()
            datatime = tr.xpath('./td[4]/span/text()').extract_first().strip()
            datatime = self.datestime(stime=datatime)
            item['INTRODUCED_stime'] = datatime
            url = 'https://security.snyk.io/' + item['url']
            item['url'] = url
            # 导入存储在类中的数据库类 查询是否在数据库中存在
            data = self.data
            self.data_max += 1
            # 校验此条数据是否存在数据库
            err = data.price_exists(field='url', price=url)
            if err['error'] == 101:
                logger.error(f"跳转详情页进行爬取{url}")
                self.repeat_num = 0
                yield scrapy.Request(url=url, callback=self.second, meta={"item": item})
            # 查询语句出错，返回信息，停止程序
            elif err['error'] == 104 or err['error'] == 103:
                logger.error(f'{response.url}数据查询失败：错误信息{err["log"]}')
                self.crawler.engine.close_spider(self, '数据库查询信息出错')
            else:
                # 数据存在情况，更新时间与当前爬取到时间比较，是否需要数据存储
                data_stime = data.query_page(field=item['url'], name='INTRODUCED_stime', fields='url')[0]
                date_obj = datetime.datetime.strptime(item['INTRODUCED_stime'], "%Y-%m-%d")
                # 有新的更新时间进行数据存储
                if data_stime < date_obj:
                    logger.error(f"详情页{url}数据有更新，跳转爬取")
                    item['PageMax'] = int(data.query_page(name='PageMax')[0]) + 1
                    yield scrapy.Request(url=url, callback=self.second, meta={"item": item})
                logger.error(f"详情页{url}数据已存在，无需更新")
                self.repeat_num += 1

        self.page += 1
        if self.page <= self.page_max:
            url = format(self.url % self.page)
            yield scrapy.Request(url=url, callback=self.parse)

    def second(self, response):
        logger.error(f'跳转详情页提取数据，详情页url：{response.url}')
        item = response.meta['item']
        item['CVE'] = str(response.xpath(
            '//*[@id="__layout"]/div/main/div/div[2]/div[3]/div[1]/div[1]/span[@class="cve"]/span/a/text()').extract_first()).strip()
        item['CWE'] = str(response.xpath(
            '//*[@id="__layout"]/div/main/div/div[2]/div[3]/div[1]/div[1]/span[@data-snyk-test="cwe"]/span/a/text()').extract_first()).strip()

        markdown_section = response.xpath(
            '//*[@id="__layout"]/div/main/div//div[@class="left"]//div[@class="markdown-section"]')

        for markdown in markdown_section:
            if "How to fix" in markdown.xpath('./h2/text()').extract_first().strip():
                item['MarkdownSection'] = ''.join(markdown.xpath('./div/div//text()').extract()).strip()
            elif "Overview" in markdown.xpath('./h2/text()').extract_first().strip():
                item['Overview'] = ''.join(markdown.xpath('./div/div//text()').extract()).strip()
            elif "References" in markdown.xpath('./h2/text()').extract_first().strip():
                item['ReferencesData'] = markdown.xpath('./div/div/ul/li/a/@href').extract()
            elif "Details" in markdown.xpath('./h2/text()').extract_first().strip():
                item['Details'] = ''.join(markdown.xpath('./div/div//text()').extract())

        if "Upgrade" in item['MarkdownSection']:
            markdown_section2 = item['MarkdownSection']
            markdown_section2 = markdown_section2.replace('Upgrade ', "").replace(' or higher.', "").split(
                ' to version ')
            markdown_section2 = f"升级{markdown_section2[0]}至{markdown_section2[1]}或更高版本."
            item['MarkdownSection'] = markdown_section2

        snyk_data = {}

        snyk_cvss_list = response.xpath('//*[@id="__layout"]/div/main//div[@class="details-box__body"]/ul/div')
        for snyk_cvss in snyk_cvss_list:
            title = str(snyk_cvss.xpath('./span[1]/text()').extract_first()).strip()
            data = str(snyk_cvss.xpath('./span[2]/strong/text()').extract_first()).strip()
            snyk_data[title] = data

        snyk_cvss_list = response.xpath('//*[@id="__layout"]/div/main//div[@class="details-box__body"]/div/div/ul/div')
        for snyk_cvss in snyk_cvss_list:
            title = str(snyk_cvss.xpath('./span[1]/text()').extract_first()).strip()
            data = str(snyk_cvss.xpath('./span[2]/strong/text()').extract_first()).strip()
            snyk_data[title] = data
        item['SnykCVSS'] = json.dumps(snyk_data)

        Red_data = {}

        Red_Hat_list = response.xpath('//*[@id="__layout"]/div/main//div[@class="vendorcvss"]/div/div[2]/div/div/div')
        for Red_Hat in Red_Hat_list:
            title = str(Red_Hat.xpath('./span[1]/text()').extract_first()).strip()
            data = str(Red_Hat.xpath('./span[2]/strong/text()').extract_first()).strip()
            Red_data[title] = data
        item['RedHat'] = json.dumps(Red_data)
        logger.error(f'通过item对象判断地址：{item["url"]}是否需要下钻爬取')
        if item.get('second_url'):
            url = 'https://security.snyk.io' + item['second_url']
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.second_db, dont_filter=True)
        else:
            yield item

    def second_db(self, response):

        item = response.meta['item']
        sink_one_url_list = response.xpath('//*[@id="__layout"]/div/main//div[@class="vue--card__body"]/div/ul/li')
        sink_data = {}
        for li in sink_one_url_list:
            key = li.xpath('./h3/text()').extract_first()
            if li.xpath('./div/a').extract_first():
                value = li.xpath('./div/a/@href').extract()
            else:
                value = ''.join(li.xpath('./h3/following-sibling::*[1]//text()').extract()).strip()

            if not key:
                key = 'url'
            sink_data[key] = value
        item['sink_one_data'] = json.dumps(sink_data)
        logger.error(f'通过item对象判断地址：{response.url}是否需要二次下钻爬取')
        if sink_data.get('url'):
            yield scrapy.Request(url=sink_data['url'][0], meta={'item': item}, callback=self.secondary,
                                 dont_filter=True)
        else:
            yield item

    def secondary(self, response):
        item = response.meta['item']
        try:
            logger.error(f'二次下钻爬取：{item["url"]}')
            sink_two_data = response.xpath(
                '//*[@id="__layout"]/div/div/div//header[@class="header"]/div/div/div/input/@value').extract_first()
            item['sink_two_data'] = sink_two_data
        except:
            yield item
        else:
            yield item

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

        stime[1] = str(date[stime[1]])
        # stime = [stime[2], stime[0], stime[1]]
        # return stime
        return '-'.join(stime[::-1])
