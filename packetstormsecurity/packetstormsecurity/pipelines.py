# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import logging

from packetstormsecurity.id_tool.id_generator import IdGenerator
from packetstormsecurity.id_tool.id_seq import IdSeq
from packetstormsecurity.items import PacketstormsecurityItem
from packetstormsecurity.toolclass.OperateDB import MysqlData
from packetstormsecurity.toolclass.proxy_module import GetProxy

from packetstormsecurity import settings

# 实例化日志类
logger = logging.getLogger(__name__)


class DataPipeline:

    def open_spider(self, spider):

        h = GetProxy()
        settings.PROXY_HTTPS = h.proxies_data()

        host = settings.MYSQL_HOST
        user = settings.MYSQL_USER
        pwd = settings.MYSQL_PWD
        port = settings.MYSQL_PORT
        db = settings.MYSQL_DB
        tb = settings.MYSQL_TB
        self.data = MysqlData()
        self.data.connect_data(host=host, user=user, password=pwd, port=port)
        # 连接成功数据库，进入数据库和查看表结构
        logger.error(self.data.data_exists(data=db))
        logger.error(self.data.table_exists(table=tb))
        # 数据库和数据表存在或创建完成后,传入item对象，创建剩余的字段结构
        logger.error(self.data.field_exists(fields=vars(PacketstormsecurityItem)['fields']))
        spider.data_max = 0
        spider.data = self.data
        spider.max = 0
        settings.data_page = self.data.query_page()

    def process_item(self, item, spider):
        ID = IdGenerator(IdSeq.coresecurity.value)
        err = self.data.price_exists(field='id', price=item['id'])
        while err['error'] == 102:
            item['id'] = ID.get_id()
            err = self.data.price_exists(field='id', price=item['id'])

        fields = vars(PacketstormsecurityItem)['fields']
        for field in fields:
            if field == 'url' or "time" in field:
                continue
            elif field == "id":
                item[field] = str(item[field])
            elif item.get(field):
                item[field] = json.dumps(item[field])
            else:
                item[field] = None
        i = 0
        while i < 3:
            err = self.data.add_data(item=item)
            if "数据实例化存储成功" in err:
                break
            item['id'] = ID.get_id()
            i += 1
        # print(item)
        logger.error(item['url'] + err)
        return item

    def close_spider(self, spider):

        logger.error(f"数据总量为{spider.data_max},共有{spider.max}条详情页无数据")
        logger.error(self.data.disconnect())
