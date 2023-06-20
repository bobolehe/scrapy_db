import datetime
import json
import logging

import scrapy
from nvdPro.id_tool.id_generator import IdGenerator
from nvdPro.id_tool.id_seq import IdSeq
from nvdPro.items import NvdproItem
from nvdPro import settings

# 实例化日志类
logger = logging.getLogger(__name__)


class NvdSpider(scrapy.Spider):
    name = "nvd"
    log = None
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://services.nvd.nist.gov/rest/json/cves/2.0/?resultsPerPage=40&startIndex=74160"]
    url = 'https://services.nvd.nist.gov/rest/json/cves/2.0/?resultsPerPage=40&startIndex=%d'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.MYSQL_HOST = kwargs.get('host') if kwargs.get('host') else settings.MYSQL_HOST
        settings.MYSQL_USER = kwargs.get('user') if kwargs.get('user') else settings.MYSQL_USER
        settings.MYSQL_PWD = kwargs.get('pwd') if kwargs.get('pwd') else settings.MYSQL_PWD
        settings.MYSQL_PORT = kwargs.get('port') if kwargs.get('port') else settings.MYSQL_PORT
        settings.MYSQL_DB = kwargs.get('db') if kwargs.get('db') else settings.MYSQL_DB
        settings.MYSQL_TB = kwargs.get('tb') if kwargs.get('tb') else settings.MYSQL_TB
        self.page_max = int(kwargs.get('page')) if kwargs.get('page') else 0
        self.page = 74160

    def parse(self, response):
        if response.status == 404:
            yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True)

        logger.error(f"爬取分页{response.url} 下数据")
        totalResults = json.loads(response.text)['totalResults']
        resultsPerPage = json.loads(response.text)['resultsPerPage']
        startIndex = json.loads(response.text)['startIndex']
        nvd_list = json.loads(response.text)['vulnerabilities']

        if not nvd_list:
            self.log = '数据达到最大值'
            logger.error(f'数据达到最大值')
            self.crawler.engine.close_spider(self, '数据达到最大值')
            return

        for nvd in nvd_list:
            try:
                cve_data = nvd['cve']
                cve = cve_data['id']
                descriptions_list = cve_data['descriptions']
                description = None
                for d in descriptions_list[0:1]:
                    description = d['value']
                published = cve_data['published']
                published = datetime.datetime.fromisoformat(published)
                lastModified = cve_data['lastModified']
                lastModified = datetime.datetime.fromisoformat(lastModified)
                # references = cve_data['references']
                hyper = [i['url'] for i in cve_data['references']]

                # 获取cvss2
                # 获取cvss3
                cvss2 = None
                cvss3 = None
                for name in cve_data['metrics']:
                    if "cvssMetricV2" in name:
                        cvss2 = cve_data['metrics'].get(name, None)
                    elif "cvssMetricV3" in name:
                        cvss3 = cve_data['metrics'].get(name, None)
                # 获取cpe
                configurations = cve_data.get('configurations', [])
                cpe_list = []
                for nodes in configurations:
                    for node in nodes['nodes']:
                        for cpe in node['cpeMatch']:
                            cpe_list.append(cpe)
                # 获取cwe
                weaknesses = cve_data.get('weaknesses', [])
                cwe = []
                for weak in weaknesses:
                    for cwe_list in weak['description']:
                        cwe.append(cwe_list['value'])
                if "NVD-CWE-Other" in cwe:
                    cwe.remove("NVD-CWE-Other")
                elif "NVD-CWE-noinfo" in cwe:
                    cwe.remove("NVD-CWE-noinfo")
                cwe = ','.join(cwe)
            except Exception as e:
                self.log = f'解析 json数据失败，{e}'
                logger.error(f'解析 json数据失败，{e}')
                self.crawler.engine.close_spider(self, f'解析 json数据失败，{e}')
            else:
                item = NvdproItem()
                ID = IdGenerator(IdSeq.coresecurity.value)
                item['id'] = ID.get_id()
                item['cve'] = cve
                item['description'] = description
                item['cve_published_time'] = published
                item['cve_last_modified_time'] = lastModified
                item['hyper'] = hyper
                item['cwe'] = cwe
                item['cpe'] = cpe_list
                item['cvss2'] = cvss2
                item['cvss3'] = cvss3
                item['update_time'] = str(datetime.datetime.now())
                item['last_modified_time'] = str(datetime.datetime.now())
                item['create_time'] = str(datetime.datetime.now())
                item['update_num'] = 1
                # 数据总数加1
                self.data_max += 1
                yield item

        if self.page_max:
            if self.page <= self.page_max:
                page_num = resultsPerPage * self.page
                page_num = totalResults - page_num
                url = format(self.url % page_num)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
                self.page += 1
        else:
            page_num = startIndex + resultsPerPage
            url = format(self.url % page_num)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
