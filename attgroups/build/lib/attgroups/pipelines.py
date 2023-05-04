# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import logging
import datetime
from attgroups import settings

# 实例化日志类
logger = logging.getLogger(__name__)


class AttgroupsPipeline:

    def open_spider(self, spider):
        host = settings.MYSQL_HOST
        user = settings.MYSQL_USER
        pwd = settings.MYSQL_PWD
        port = settings.MYSQL_PORT
        db = settings.MYSQL_DB

        try:
            self.db = mysql.connector.connect(host=host, user=user, password=pwd, port=port, db=db)
            self.cursor = self.db.cursor()
            spider.db = self.cursor
            spider.data_max = 0
            print("数据库链接成功")
            logger.error("数据库链接成功")
            self.ks_time = str(datetime.datetime.now())
        except:
            logger.error("数据库链接失败")

    def process_item(self, item, spider):
        spiderDate = datetime.datetime.now()
        spiderDate = str(spiderDate)

        self.sql = "insert into attgroups(GroupsName,GroupsId,AssociatedGroups,Created,LastModified,AssociatedGroupDescriptions,Techniques,Softwart,Datatime,url) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

        try:
            self.cursor.execute(self.sql, (
                item['name'], item['title_id'], item['Associated_Groups'], item['Created'],
                item['Last_Modified'], item['Associated_Group_Descriptions'], item['Techniques_Used'], item['Software'],
                spiderDate, item['url']
            ))

            self.sql = self.sql.format((item['name'], item['title_id'], item['Associated_Groups'], item['Created'],
                                        item['Last_Modified'], item['Associated_Group_Descriptions'],
                                        item['Techniques_Used'], item['Software'],
                                        spiderDate))
            self.db.commit()
            print(f'链接详情已实例化存储:{item["url"]}')
            logger.error(f'链接详情已实例化存储:{item["url"]}')

        except:
            self.db.rollback()
            print(f'sql语句实例化存储失败,失败地址:{item["url"]}')
            logger.error(f'sql语句实例化存储失败,失败地址:{item["url"]}')

        return item

    def close_spider(self, spider):
        try:
            sql = f"SELECT * FROM attgroups WHERE Datatime >= '{self.ks_time}';"
            # sql = "SELECT * FROM eol WHERE stime >= '2023-04-11 17:16:10';"
            # print(sql)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            print(f"此次添加{len(result)}条数据,共{spider.data_max}条数据")
            logger.error(f"此次添加{len(result)}条数据,共{spider.data_max}条数据")
        except:
            logger.error(f'数据查询添加数量失败关闭,执行时间为{self.ks_time}')
            print(f'数据查询添加数量失败关闭，执行时间为{self.ks_time}')
            self.cursor.close()
            self.db.close()
            print('数据链接关闭')
        else:
            self.cursor.close()
            self.db.close()
            logger.error('数据链接关闭')
            print('数据链接关闭')
