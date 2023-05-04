# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
from attgroups.items import AttgroupsItem
from attgroups import settings
from attgroups.linkData import MysqlData

# 实例化日志类
logger = logging.getLogger(__name__)


class DataPipeline:

    def open_spider(self, spider):
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
        logger.error(self.data.field_exists(fields=vars(AttgroupsItem)['fields']))
        spider.data_max = 0
        spider.data = self.data

    def process_item(self, item, spider):
        logger.error(item['url'] + self.data.add_data(item=item))
        return item

    def close_spider(self, spider):
        logger.error(f"数据总量为{spider.data_max}")
        logger.error(self.data.disconnect())
