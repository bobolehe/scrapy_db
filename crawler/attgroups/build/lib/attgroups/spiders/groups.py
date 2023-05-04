import json
import re
import scrapy
import logging
from attgroups.items import AttgroupsItem
from attgroups import settings

# 实例化日志类
logger = logging.getLogger(__name__)


class GroupsSpider(scrapy.Spider):
    name = "groups"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://attack.mitre.org/groups/"]

    def __init__(self, host='127.0.0.1', user='root', password='123456', port=3306, db="spider", *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.MYSQL_HOST = host
        settings.MYSQL_USER = user
        settings.MYSQL_PWD = password
        settings.MYSQL_PORT = port
        settings.MYSQL_DB = db

    def parse(self, response):
        logger.error("爬取详情页名称与链接")
        # .extract_first()
        sidenav_list = response.xpath('//*[@id="v-tab"]/div[1]/div/div[@class="sidenav-list"]/div')
        for sidenav in sidenav_list:
            item = AttgroupsItem()
            item['name'] = sidenav.xpath('./div/a/text()').extract_first().strip()

            if not sidenav.xpath('./div/@id').extract_first() == "0-0":
                # print(sidenav.xpath('./div/a/@href').extract_first())
                url = 'https://attack.mitre.org' + sidenav.xpath('./div/a/@href').extract_first()
                # 导入存储在类中的数据库类 查询是否在数据库中存在
                db = self.db
                self.data_max += 1
                # 校验此条数据是否存在数据库
                sql = f"select url from attgroups where url='{url}';"
                db.execute(sql)
                result = db.fetchone()
                if not result:
                    print(f"跳转详情页进行爬取{url}")
                    logger.error(f"跳转详情页进行爬取{url}")
                    yield scrapy.Request(url=url, meta={'item': item}, callback=self.url_row, dont_filter=True)
                logger.error(f"{url}数据已存在")

    def url_row(self, response):
        try:
            item = response.meta['item']
            item['url'] = response.url
            description_body = response.xpath(
                '//*[@id="v-attckmatrix"]/div[@class="row"]//div[@class="description-body"]/p//text()').extract()
            description_data = list(description_body)
            for index, description in enumerate(description_body):
                if re.match(r"\[\d*]", description):
                    description_data.remove(description_body[index])
            item['description_body'] = "".join(description_data)

            item['title_id'] = ''.join(response.xpath('//*[@id="card-id"]/div/text()').extract()).strip()

            card_data_list = response.xpath('//*[@id="card-id"]/following-sibling::*')
            for card_data in card_data_list:
                title = ''.join(card_data.xpath('./div/span//text()').extract()).strip()
                if "Created" in title:
                    item['Created'] = ''.join(card_data.xpath('./div/text()').extract()).strip()
                elif "Last Modified" in title:
                    item['Last_Modified'] = ''.join(card_data.xpath('./div/text()').extract()).strip()
                elif "Associated Groups" in title:
                    item['Associated_Groups'] = ''.join(card_data.xpath('./div/text()').extract()).strip().replace(': ',
                                                                                                                   "")
            item['Associated_Groups'] = item['Associated_Groups'] if item.get('Associated_Groups') else "None"
            item['Created'] = item['Created'] if item.get('Created') else "None"
            item['Last_Modified'] = item['Last_Modified'] if item.get('Last_Modified') else "None"

            # 获取 Associated Group Descriptions
            aliasDescription_list = response.xpath('//*[@id="aliasDescription"]/following-sibling::table[1]/tbody/tr')
            aliasDescription = []
            for tr in aliasDescription_list:
                name = tr.xpath('./td[1]/text()').extract_first().strip()
                Description_url = ' '.join(tr.xpath('./td[2]//span//a/@href').extract())
                Description = ''.join(tr.xpath('./td[2]/p//text()').extract()) + Description_url
                aliasDescription.append({"name": name, "Description": Description})
            if not aliasDescription:
                aliasDescription = 'None'
            item['Associated_Group_Descriptions'] = json.dumps(aliasDescription)

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
            item['Techniques_Used'] = json.dumps(techniques)

            # 获取Software内容
            Software_list = response.xpath('//*[@id="software"]/following-sibling::table[1]/tbody/tr')
            Software = []
            for software in Software_list:
                ID = software.xpath('./td[1]/a/text()').extract_first()
                Name = software.xpath('./td[2]/a/text()').extract_first()
                References = software.xpath('./td[3]//a/@href').extract()
                Techniques = ''.join(software.xpath('./td[4]//a/text()').extract())
                Software.append({'ID': ID, 'Name': Name, 'References': References, 'Techniques': Techniques})
            item['Software'] = json.dumps(Software)

            yield item

        except:
            logger.error(f"{response.url}数据缓存失败")
