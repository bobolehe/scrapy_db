封装数据库操作方法，原因：避免在爬虫程序中出现sql等数据库操作语句



封装后的数据库方法 OperateDB模块中MysqlData封装mysql数据库的基本操作



SpidersTemplate爬虫程序为使用封装方法案例

主要使用需要在settings配置文件中添加指定参数作为程序执行时接收参数使用

```python
# mysql配置信息
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PWD = "123456"
MYSQL_PORT = 3306
MYSQL_DB = "spiders"
MYSQL_TB = 'attgroups'
```

这么参数为默认数据库操作参数

在爬虫程序spider文件中可使用,这种方式实现接收指定名称的键转换为参数

```python
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.MYSQL_HOST = kwargs.get('host') if kwargs.get('host') else settings.MYSQL_HOST
        settings.MYSQL_USER = kwargs.get('user') if kwargs.get('user') else settings.MYSQL_USER
        settings.MYSQL_PWD = kwargs.get('pwd') if kwargs.get('pwd') else settings.MYSQL_PWD
        settings.MYSQL_PORT = kwargs.get('port') if kwargs.get('port') else settings.MYSQL_PORT
        settings.MYSQL_DB = kwargs.get('db') if kwargs.get('db') else settings.MYSQL_DB
        settings.MYSQL_TB = kwargs.get('tb') if kwargs.get('tb') else settings.MYSQL_TB
        self.page_max = kwargs.get('page') if kwargs.get('page') else 10
```

在管道类中就可使用封装好的数据库操作类

```
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
        rute = self.data.connect_data(host=host, user=user, password=pwd, port=port)
        # 连接成功数据库，进入数据库和查看表结构
        print(self.data.data_exists(data=db))
        print(self.data.table_exists(table=tb))
        # 数据库和数据表存在或创建完成后,传入item对象，创建剩余的字段结构
        print(self.data.field_exists(fields=vars(AttgroupsItem)['fields']))
		# 这里是先爬虫文件传递属性使用
        spider.data_max = 0
        spider.data = self.data

    def process_item(self, item, spider):
        print(self.data.add_data(item=item))
        return item

    def close_spider(self, spider):
        logger.error(f"数据总量为{spider.data_max}")
        logger.error(self.data.disconnect())
```

在爬虫文件中

```
class GroupsSpider(scrapy.Spider):
    name = "groups"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://attack.mitre.org/groups/"]

    def parse(self, response):
        # 调用管道类为其添加的属性
        data = self.data
        self.data_max += 1

```

使用封装方法进行爬虫程序编写时需注意：

​		item类中定义字段名称需要复核python规范还需要复核mysql创建字段规范

