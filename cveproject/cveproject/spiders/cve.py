import datetime
import json
import logging

import scrapy
from cveproject import settings
from cveproject.id_tool.id_generator import IdGenerator
from cveproject.id_tool.id_seq import IdSeq
from cveproject.items import CveprojectItem

# 实例化日志类
logger = logging.getLogger(__name__)


class CveSpider(scrapy.Spider):
    name = "cve"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://github.com/CVEProject/cvelist/tree-commit-info/master"]
    # start_urls = ["https://github.com/CVEProject/cvelist/tree-commit-info/master/2002/0xxx"]
    url = 'https://github.com/CVEProject/cvelist/tree-commit-info/master'
    failed_requests = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.MYSQL_HOST = kwargs.get('host') if kwargs.get('host') else settings.MYSQL_HOST
        settings.MYSQL_USER = kwargs.get('user') if kwargs.get('user') else settings.MYSQL_USER
        settings.MYSQL_PWD = kwargs.get('pwd') if kwargs.get('pwd') else settings.MYSQL_PWD
        settings.MYSQL_PORT = kwargs.get('port') if kwargs.get('port') else settings.MYSQL_PORT
        settings.MYSQL_DB = kwargs.get('db') if kwargs.get('db') else settings.MYSQL_DB
        settings.MYSQL_TB = kwargs.get('tb') if kwargs.get('tb') else settings.MYSQL_TB
        self.page_max = int(kwargs.get('page')) if kwargs.get('page') else 0
        self.page = 1
        self.data_time = None

    def parse(self, response):
        # .extract_first()
        # with open('源码.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        logger.error(f"{response.url}")
        grouping_dict = json.loads(response.text)

        if grouping_dict.get('error'):
            logger.error(f"{response.url}访问有误或无数据")
            return

        if response.url in self.failed_requests:
            self.failed_requests.remove(response.url)

        if not self.data_time:
            data = self.data
            self.data_time = data.query_page(table='cvetest', name='data_update_time')[0]

        key_list = [i for i in grouping_dict]

        for row in key_list:
            url = response.url + f"/{row}"
            if str(row).endswith('json'):
                item = CveprojectItem()
                data_update_time = grouping_dict[row]['date']
                data_update_time = datetime.datetime.fromisoformat(data_update_time[0:23])
                if data_update_time > self.data_time:
                    item['data_update_time'] = str(data_update_time)
                    url = 'https://raw.githubusercontent.com/CVEProject/cvelist' + str(url).split('tree-commit-info')[1]
                    print(url, "有更新")
                    yield scrapy.Request(url=url, callback=self.data_spider, dont_filter=True,
                                         meta={'download_timeout': 30, 'item': item})
            else:
                data_update_time = grouping_dict[row]['date']
                data_update_time = datetime.datetime.fromisoformat(data_update_time[0:23])
                # print('数据时间', data_update_time)
                # print("数据库时间", self.data_time)
                if not self.data_time:
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={'download_timeout': 30})
                elif data_update_time > self.data_time:
                    print(url, "有更新")
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={'download_timeout': 30})

    def data_spider(self, response):

        logger.error(f'解析{response.url}下JSON数据')
        if response.url in self.failed_requests:
            self.failed_requests.remove(response.url)

        item = response.meta['item']
        cve = json.loads(response.text)
        ID = IdGenerator(IdSeq.coresecurity.value)
        item['data_time'] = str(datetime.datetime.now())
        item['id'] = ID.get_id()
        item['url'] = response.url
        for k, v in cve.items():
            if k == "CVE_data_meta":
                item['cve_id'] = cve[k]['ID']
                item['cve_state'] = cve[k]['STATE']
            else:
                item[k] = v
        # 数据总数加1
        self.data_max += 1
        # 导入存储在类中的数据库类 查询是否在数据库中存在
        data = self.data
        # logger.error(f"校验{url}连接数据是否需要实例化存储")
        err = self.VerificationData(Mdata=data, item=item, response=response)
        if err:
            yield item
        else:
            logger.error(f"{response.url}数据已是最新内容，无需实例化")

    def VerificationData(self, Mdata, item, response):
        """
        数据库校验数据
        :param self:
        :param Mdata:
        :param item:
        :param response:
        :return:
        """
        try:
            result = None
            # 校验数据是否存在数据库
            err = Mdata.price_exists(field='cve_id', price=item['cve_id'], table=settings.MYSQL_TB)
            # 不存在数据库，直接进行存储
            if err['error'] == 101:
                return item
            # 查询语句出错，返回信息，停止程序
            elif err['error'] == 104 or err['error'] == 103:
                logger.error(f'{item["url"]}数据查询失败：错误信息{err["log"]}')
                self.crawler.engine.close_spider(self, '数据库查询信息出错')
            elif err['error'] == 102:
                result = err['data']

            # 查询数据库中已有数据的数据更新时间
            data_stime = \
                Mdata.query_page(field=item['cve_id'], name='data_update_time', fields='cve_id',
                                 table=settings.MYSQL_TB)[0]
            # 没有数据更新时间，再次进行存储
            if not data_stime:
                for i in result[0]:
                    logger.error(Mdata.delete_data(table=settings.MYSQL_TB, field='id', price=i))
                logger.error(f'{item["url"]}数据存在,但无更新日期，进行更新')
                return item
            # 存在更新时间与当前爬取到时间比较，是否需要数据存储
            date_obj = datetime.datetime.strptime(item['data_update_time'], "%Y-%m-%d %H:%M:%S")
            # 有新的更新时间进行数据存储
            if data_stime < date_obj:
                for i in result[0]:
                    logger.error(Mdata.delete_data(table=settings.MYSQL_TB, field='id', price=i))
                logger.error(f'更新{item["url"]}数据')
                return item

        except Exception as e:
            logger.error(f"数据库校验数据失败，错误信息{e}")
