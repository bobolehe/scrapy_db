import scrapy
import re
import json
import logging
import datetime
from attsoftware import settings
from attsoftware.items import AttsoftwareItem

# 实例化日志类
logger = logging.getLogger(__name__)


class SoftwareSpider(scrapy.Spider):
    name = "software"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://attack.mitre.org/software/"]

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
        # .extract_first()
        logger.error("抓取详情页地址")
        sidenav_list = response.xpath('//*[@id="v-tab"]/div[1]/div/div[@class="sidenav-list"]/div')
        for sidenav in sidenav_list:
            item = AttsoftwareItem()
            item['name'] = json.dumps(sidenav.xpath('./div/a/text()').extract_first().strip())

            if not sidenav.xpath('./div/@id').extract_first() == "0-0":
                # print(sidenav.xpath('./div/a/@href').extract_first())

                url = 'https://attack.mitre.org' + sidenav.xpath('./div/a/@href').extract_first()
                logger.error(f"爬取到名称{item['name']}地址{url}")
                item['url'] = url
                self.data_max += 1
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.url_row, dont_filter=True)

    def url_row(self, response):
        try:
            item = response.meta['item']
            description_body = response.xpath(
                '//*[@id="v-attckmatrix"]/div[@class="row"]//div[@class="description-body"]/p//text()').extract()
            description_data = list(description_body)
            for index, description in enumerate(description_body):
                if re.match(r"\[\d*]", description):
                    description_data.remove(description_body[index])
            item['description_body'] = json.dumps("".join(description_data))

            card_data_list = response.xpath(
                '//*[@id="v-attckmatrix"]//div[@class="row"]//div[@class="card-body"]/div/div[2]')
            card = {}
            for card_data in card_data_list:
                key = ''.join(card_data.xpath('./span/text()').extract()).replace(":", "").strip()
                value = ''.join(card_data.xpath('./text()').extract()).replace(":", "").strip()
                card[key] = value
            item["card"] = card
            item['software_id'] = card['ID']
            item['uptodate_time'] = self.datestime(card['Last Modified'])

            # 导入存储在类中的数据库类 查询是否在数据库中存在
            data = self.data
            err = self.VerificationData(Mdata=data, item=item, response=response)
            if not err:
                logger.error(f"{response.url}数据已是最新内容，无需实例化")
                return

            # 获取techniques内容
            techniques_list = response.xpath('//*[@id="techniques"]/following-sibling::table[1]/tbody/tr')
            techniques = []
            for tr in techniques_list:
                td_list = tr.xpath('./td')
                if len(td_list) == 5:
                    Domain = td_list[0].xpath('./text()').extract_first()
                    Domain = Domain.strip() if Domain else "None"
                    if not (Domain == "None"):
                        id = ''.join(td_list[1:3].xpath('./a/text()').extract())
                    else:
                        Domain = techniques[-1]['Domain']
                        id_home = str(techniques[-1]['id']).split('.')[0]
                        id = id_home + ''.join(td_list[2:3].xpath('./a/text()').extract())
                    Name = ''.join(td_list[-2].xpath('.//text()').extract()).strip()
                    url_list = td_list[-1].xpath('./p/span//a')
                    Use_url = {}
                    for url in url_list:
                        Use_url[url.xpath('./text()').extract_first()] = url.xpath('./@href').extract_first()
                    Use = "".join(td_list[-1].xpath('.//text()').extract()).strip()
                    for key in Use_url:
                        word1 = str(key)
                        word2 = Use_url[key]
                        Use = Use.replace(word1, word2)

                    techniques.append({"Domain": Domain, "id": id, "Name": Name, "Use": Use})
                elif len(td_list) == 4:
                    Domain = td_list[0].xpath('./text()').extract_first()
                    Domain = Domain.strip() if Domain else "None"
                    id = td_list[1].xpath('./a/text()').extract_first()
                    Name = ''.join(td_list[2].xpath('.//text()').extract()).strip()
                    url_list = td_list[3].xpath('./p/span//a')
                    Use_url = {}
                    for url in url_list:
                        Use_url[url.xpath('./text()').extract_first()] = url.xpath('./@href').extract_first()
                    Use = "".join(td_list[3].xpath('.//text()').extract()).strip()
                    for key in Use_url:
                        word1 = str(key)
                        word2 = Use_url[key]
                        Use = Use.replace(word1, word2)
                    techniques.append({"Domain": Domain, "id": id, "Name": Name, "Use": Use})
            item['Techniques'] = json.dumps(techniques)

            # 获取Software内容
            Software_list = response.xpath('//*[@id="groups"]/following-sibling::table[1]/tbody/tr')
            Software = []
            for software in Software_list:
                ID = software.xpath('./td[1]/a/text()').extract_first()
                Name = software.xpath('./td[2]/a/text()').extract_first()
                References = software.xpath('./td[3]//a/@href').extract()
                Software.append({'ID': ID, 'Name': Name, 'References': References})
            item['Software'] = json.dumps(Software)
            item['stime'] = str(datetime.datetime.now())
            # print(item)
            yield item
        except:
            logger.error(f"{response.url}数据缓存失败")

    def datestime(self, stime):
        date = {
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

        stime[1] = str(date[stime[1]])
        stime = [stime[2], stime[1], stime[0]]
        return '-'.join(stime)

    def VerificationData(self, Mdata, item, response):
        try:
            # 校验数据是否存在数据库
            err = Mdata.price_exists(field='software_id', price=item['software_id'])
            # 不存在数据库，直接进行存储
            if err['error'] == 101:
                item['pagemax'] = 1
                return item
            # 查询语句出错，返回信息，停止程序
            elif err['error'] == 104 or err['error'] == 103:
                logger.error(f'{response.url}数据查询失败：错误信息{err["log"]}')
                self.crawler.engine.close_spider(self, '数据库查询信息出错')

            # 查询数据库中已有数据的数据更新时间
            data_stime = Mdata.query_page(field=item['software_id'], name='uptodate_time', fields='software_id')[0]

            # 没有数据更新时间，再次进行存储
            if not data_stime:
                logger.error(f'{response.url}数据存在,但无更新日期，进行更新')
                item['pagemax'] = int(Mdata.query_page(field=item['software_id'], name='pagemax', fields='software_id')[0]) + 1
                return item
            # 存在更新时间与当前爬取到时间比较，是否需要数据存储
            date_obj = datetime.datetime.strptime(item['uptodate_time'], "%Y-%m-%d")
            # 有新的更新时间进行数据存储
            if data_stime < date_obj:
                logger.error(f'更新{response.url}数据')
                item['pagemax'] = int(Mdata.query_page(field=item['software_id'], name='pagemax', fields='software_id')[0]) + 1
                return item

        except Exception as e:
            logger.error(f"数据库校验数据失败，错误信息{e}")
