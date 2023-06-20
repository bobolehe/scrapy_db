import datetime
import re

import mysql.connector


class MysqlData:
    def __init__(self):
        self.DB = None
        self.curr = None
        self.data = None
        self.table = None
        self.ks_time = datetime.datetime.now()

    def connect_data(self, host='127.0.0.1', user='root', password='123456', port=3306):
        """
        链接mysql数据库
        :param host: 连接地址：默认'127.0.0.1'
        :param user: 数据库用户名：默认“root”
        :param password:数据库密码：默认“123456”
        :param prot: 连接数据库端口3306
        :return: 返回结果，操作游标以及数据库链接对象
        """
        try:
            # 连接数据库并创建游标
            self.DB = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                # auth_plugin='mysql_native_password'
            )
            self.curr = self.DB.cursor()
        except:
            # 返回结果字典
            retu = {
                'error': "数据库连接失败"
            }
            return retu
        else:
            # 连接成功返回结果字典，携带数据库对象以及游标对象
            retu = {
                'error': "数据库链接成功",
                'cursor': self.curr,
                'db': self.DB
            }
            return retu

    def data_exists(self, data="spider"):
        """
        判断数据库是否存在进行创建
        :param data: 指定数据库游标切换
        :return: 返回提示信息
        """
        # 创建数据库的sql(如果数据库存在就不创建，防止异常)
        self.data = data
        sql = f"CREATE DATABASE IF NOT EXISTS {data}"
        try:
            # 执行创建数据库的sql
            self.curr.execute(sql)
            self.DB.commit()
        except:
            # 失败回滚，返回失败信息
            self.DB.rollback()
            return f"判断数据库{data}是否存在失败"
        else:
            # 数据库存在无需创建
            self.curr.execute(f'use {data};')
            return f"数据库{data}存在无需创建"

    def table_exists(self, table='tteexxtt'):
        """
        判断数据库表是否存在
        :param table: 指定数据表
        :return: 返回提示信息
        """
        # 列出所有表名
        self.table = table
        sql = "show tables"
        try:
            self.curr.execute(sql)
            tables = self.curr.fetchall()
        except:
            return "查询数据库表结构失败"
        else:
            # 解析查询到的数据库表
            tables_list = re.findall('(\'.*?\')', str(tables))
            tables_list = [re.sub("'", '', each) for each in tables_list]

        # 判断指定表名是否存在其中
        if table in tables_list:
            fields = {'id': {}, 'url': {}, 'stime': {}}
            return self.field_exists(fields=fields)
        else:
            # 创建表结构
            try:
                sql = f"""CREATE TABLE {table}  (
                              `id` bigint(0) NOT NULL,
                              `url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                              `stime` datetime(0) NOT NULL,
                              PRIMARY KEY (`id`) USING BTREE
                            ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
                            """
                self.curr.execute(sql)
                self.DB.commit()
                return f"数据表{table}不存在进行创建表结构成功"
            except:
                self.DB.rollback()
                return f"数据表{table}不存在进行创建表结构失败,请提供正确的spl语句"

    def disconnect(self):
        """
        关闭提供的链接以及游标
        :return: 返回提示信息
        """
        try:
            sql = f"SELECT url FROM {self.table} WHERE stime >= '{self.ks_time}';"
            # sql = "SELECT * FROM eol WHERE stime >= '2023-04-11 17:16:10';"
            self.curr.execute(sql)
            result = self.curr.fetchall()
        except:
            self.curr.close()
            self.DB.close()
            return '查询失败'
        else:
            self.curr.close()
            self.DB.close()
            return f"此次数据实例化{len(result)}"

    def create_fields(self, field=str(), fields=list()):
        """
        实现数据表字段的添加
        :return:
        """
        sql = f"ALTER TABLE `{self.data}`.`{self.table}` "
        if not len(fields):
            return "无需创建"
        try:
            for i, k in enumerate(fields):
                # 添加第一条字段依据原有字段进行添加
                if k == 'url':
                    sql_new = sql + f"ADD COLUMN `{k}` varchar(255) NULL DEFAULT '' AFTER `{field}`;"
                elif 'time' in k:
                    sql_new = sql + f"ADD COLUMN `{k}` datetime(0) NULL AFTER `{field}`;"
                    # sql_new = sql + f"ADD COLUMN `{k}` datetime(255) NULL ON UPDATE CURRENT_TIMESTAMP(255) AFTER `{field}`;"
                elif k == 'id':
                    sql_new = sql + f"ADD COLUMN `{k}` int(0) NOT NULL AUTO_INCREMENT FIRST,ADD PRIMARY KEY (`{k}`);"
                else:
                    sql_new = sql + f"ADD COLUMN `{k}` json NULL AFTER `{field}`;"
                self.curr.execute(sql_new)
                self.DB.commit()
        except:
            return f"{self.table}表结构字段添加创建失败"
        else:
            return f"{self.table}字段添加创建成功"

    def field_exists(self, fields=dict()):
        """
        接收字段，判断字段是否存在，字段存在无需操作，字段不存在自行创建
        :param fields: 接收item字典判断字段是否存在
        :param data: 指定库名
        :param table: 指定表名
        :return:
        """
        # 查询表结构所有字段
        try:
            sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s'" % (
                self.data, self.table)
            self.curr.execute(sql)
            results = self.curr.fetchall()
        except:
            return '查询数据表所有字段失败'
        # 表结构字段进行格式化
        results_list = []
        for result in results:
            results_list.append(result[0])

        if not len(fields):
            return '没有传递item参数'

        # 校验所需字段在数据表中是否存在
        fields_list = []
        for field in fields:
            if not (field in results_list):
                fields_list.append(field)

        # 待添加字段中存在需要添加字段，执行添加字段方法
        if fields_list:
            return self.create_fields(field=results_list[-1], fields=fields_list)
        else:
            return f'{self.table}表结构字段无需创建'

    def add_data(self, item):
        """
        添加数据
        :param item: 需要传递字典参数
        :return: 返回提示信息
        """
        # 将item对象的键值分别取出
        keys = sorted(list(item.keys()), key=len)
        values = [item[key] for key in keys]
        # sql = f"insert into {self.table}({','.join(keys)}) values ({','.join(values)});"
        # sql语句
        sql = f"insert into {self.table}({','.join(keys)}) values ({'%s,' * ((len(values) - 1))}%s);"
        try:
            self.curr.execute(f'use {self.data}')
            self.curr.execute(sql, tuple(values))
            self.DB.commit()
        except:
            self.DB.rollback()

            return '数据实例化存储失败' + sql % tuple(values)
        else:
            return '数据实例化存储成功'

    def price_exists(self, field=str(), price=None, field2=None, price2=None):
        """
        验证数据是否存在，指定字段，传入字段查询数据
        :param field: 传入指定字段，字符串格式
        :param price: 传入查询数据
        :return: 返回字典信息，提示信息以及状态码
        """
        if not price:
            err = {
                'error': 103,
                'log': "请传入查询数据"
            }
            return err

        if not field:
            err = {
                'error': 103,
                'log': "请指定查询数据字段名，一般使用url字段查询"
            }
            return err
        if not field2:
            sql = f"SELECT {field} FROM {self.table} where {field}=%s;"
            try:
                # 执行查询语句
                self.curr.execute(sql, (price,))
                result = self.curr.fetchall()
            except Exception as e:
                err = {
                    'error': 104,
                    'log': f'{field}字段 数据查询失败{str(e)}'
                }
                return err
            if result:
                err = {
                    'error': 102,
                    'log': f'{price}数据已存在'
                }
            else:
                err = {
                    'error': 101,
                    'log': f'无{price}链接数据'
                }
            return err
        else:
            if not price2:
                err = {
                    'error': 103,
                    'log': "请指定查询数据字段名，一般使用url字段查询"
                }
                return err

    def query_page(self, field=None, name=None, fields=None):
        """
        增量式更新功能情况
        :param name: 指定页数字段名称
        :param fields: 对于数据库中抓取多个类型的url时候可以使用
        :param field: 增加判断条件，比如满足字段pro下的值为coles的数据再进行判断页数字段的最大值
        :return:
        """

        if fields:
            sql = f'SELECT MAX({name}) FROM {self.table} WHERE {fields} = "{field}";'

            try:
                # 执行查询语句
                self.curr.execute(sql)
                result = self.curr.fetchall()
                # result = self.curr.fetchone()
            except:

                return 404
            else:
                result_list = [row for row in result]
                result_list = [row for row in result_list[0]]
                return result_list
        else:
            sql = f"SELECT MAX({name}) FROM {self.table};"

            try:
                # 执行查询语句
                self.curr.execute(sql)
                # result = self.curr.fetchall()
                result = self.curr.fetchall()
            except:
                return 404
            else:
                result_list = [row for row in result]
                result_list = [row for row in result_list[0]]
                return result_list


if __name__ == '__main__':
    data = MysqlData()
    retu = data.connect_data()
    print(retu)
    if retu.get('db'):
        # 连接成功数据库，进入数据库和查看表结构
        # print(data.data_exists(data='spiders'))
        # print(data.table_exists(table='attgroups'))
        # t = str(datetime.datetime.now())
        # 测试item数据
        # 关闭数据库
        print(data.disconnect())

    coor = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        port=3306,
        db='spiders'
        # auth_plugin='mysql_native_password'
    )

    print(coor)
    coor.close()