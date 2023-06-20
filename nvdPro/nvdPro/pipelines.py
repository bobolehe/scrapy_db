# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import datetime
import json
# useful for handling different item types with a single interface
import logging
import time

from nvdPro.id_tool.id_generator import IdGenerator
from nvdPro.id_tool.id_seq import IdSeq
from nvdPro.toolclass.OperateDB import MysqlData
from nvdPro.toolclass.proxy_module import GetProxy

from nvdPro import settings

# 实例化日志类
logger = logging.getLogger(__name__)


class DataPipeline:
    # 程序启动执行
    def open_spider(self, spider):
        try:
            h = GetProxy()
            settings.PROXY_HTTPS = h.run()
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
        except Exception as e:
            spider.log = f'链接数据库失败，错误信息{e}'
            logger.error(f'链接数据库失败，错误信息{e}')
            spider.crawler.engine.close_spider(spider, f'链接数据库失败，错误信息{e}')
        spider.data_max = 0
        spider.data = self.data
        spider.max = 0
        # 定义初始数据库参数
        self.nvd = 0
        self.cwe = 0
        self.cpe = 0
        self.cvss2 = 0
        self.cvss3 = 0

    # 保存数据
    def process_item(self, item, spider):
        ID = IdGenerator(IdSeq.coresecurity.value)
        # 封装nvd数据，主要校验数据表是否存在
        if self.nvd <= 1:
            logger.error(self.data.table_exists(table='nvd'))
        nvd_data = {
            'id': item['id'], 'cve': item['cve'], 'description': item['description'],
            'cve_published_time': item['cve_published_time'],
            'cve_last_modified_time': item['cve_last_modified_time'],
            'hyper': item['hyper'], 'create_time': item['create_time'],
            'update_time': item['update_time'],
        }
        if self.nvd <= 1:
            logger.error(self.data.field_exists(fields=nvd_data.keys(), table='nvd'))
            self.nvd += 1
        err = self.data.price_exists(field='id', price=nvd_data['id'], table='nvd')
        while err['error'] == 102:
            nvd_data['id'] = ID.get_id()
            item['id'] = nvd_data['id']
            err = self.data.price_exists(field='id', price=nvd_data['id'], table='nvd')

        nvd = {}
        for field in nvd_data:
            if field == 'url' or "time" in field:
                nvd[f"`{field}`"] = nvd_data[field]
            elif field == "id":
                nvd[f"`{field}`"] = str(nvd_data[field])
            elif nvd_data.get(field):
                nvd[f"`{field}`"] = json.dumps(nvd_data[field])
        # logger.error(f"校验数据是否需要实例化存储")
        err = self.VerificationData(item=nvd_data)
        try:
            if err:
                logger.error(f'{item["cve"]}nvd表结构 {item["cve"]}' + self.data.add_data(item=nvd, table='nvd'))
                self.add_cwe(ID=ID, item=item)
                time.sleep(1)
                self.add_cpe(ID=ID, item=item)
                self.add_cvss2(ID=ID, item=item)
                self.add_cvss3(ID=ID, item=item)
            else:
                logger.error(f"{item['cve']}数据已是最新内容，无需实例化")
        except Exception as e:
            logger.error(f'{item["cve"]}数据存储失败，错误信息{e}')
        return item

    # 向cwe表添加数据方法
    def add_cwe(self, ID, item):
        # 确定数据表存在
        if self.cwe <= 1:
            logger.error(self.data.table_exists(table='nvd_cwe'))
        # 判断cve数据是否存在，存在则删除
        err = self.data.price_exists(field='cve', price=item['cve'], table='nvd_cwe')
        if err['error'] == 102:
            cwe_id = err['data'][0]
            for i in cwe_id:
                logger.error("cwe表数据:" + self.data.delete_data(table='nvd_cwe', field='id', price=i))

        # 梳理数据
        cwe_data = {
            'id': item['id'],
            'cve': item['cve'],
            'cwe': item['cwe'],
            'update_time': item['create_time'],
        }

        if not cwe_data['cwe']:
            return logger.error(f'{item["cve"]} 无cwe数据')

        err = self.data.price_exists(field='id', price=cwe_data['id'], table='nvd_cwe')
        while err['error'] == 102:
            cwe_data['id'] = ID.get_id()
            err = self.data.price_exists(field='id', price=cwe_data['id'], table='nvd_cwe')
        # 数据表添加字段
        if self.cwe <= 1:
            logger.error(self.data.field_exists(fields=cwe_data.keys(), table='nvd_cwe'))
            self.cwe += 1
        cwedata = {}
        for field in cwe_data:
            if field == 'url' or "time" in field:
                cwedata[f"`{field}`"] = cwe_data[field]
            elif field == "id":
                cwedata[f"`{field}`"] = str(cwe_data[field])
            elif cwe_data.get(field):
                cwedata[f"`{field}`"] = json.dumps(cwe_data[field])

        return logger.error(f'cwe数据表 {item["cve"]}' + self.data.add_data(item=cwedata, table='nvd_cwe'))

    # 添加cpe数据方法
    def add_cpe(self, ID, item):
        # 向cpe表和cpe_relation表中添加数据
        if self.cpe <= 1:
            logger.error(self.data.table_exists(table='nvd_cpe_all'))
            logger.error(self.data.table_exists(table='nvd_cpe_relation'))
        cpe_data_all = item['cpe'] if item['cpe'] else []
        for cpe_data in cpe_data_all:
            cpe = {'id': ID.get_id(),
                   'cpe': cpe_data['criteria'],
                   'part': str(cpe_data['criteria']).split(':')[2],
                   'vendor': str(cpe_data['criteria']).split(':')[3],
                   'product': str(cpe_data['criteria']).split(':')[4],
                   'version': str(cpe_data['criteria']).split(':')[5],
                   'update': str(cpe_data['criteria']).split(':')[6],
                   'edition': str(cpe_data['criteria']).split(':')[7],
                   'language': str(cpe_data['criteria']).split(':')[8],
                   'update_time': item['create_time']
                   }
            err = self.data.price_exists(field='id', price=cpe['id'], table='nvd_cpe_all')
            while err['error'] == 102:
                cpe['id'] = ID.get_id()
                err = self.data.price_exists(field='id', price=cpe['id'], table='nvd_cpe_all')
            cpedata = {}
            for field in cpe:
                if field == 'url' or "time" in field:
                    cpedata[f"`{field}`"] = cpe[field]
                elif field == "id":
                    cpedata[f"`{field}`"] = str(cpe[field])
                elif cpe.get(field):
                    cpedata[f"`{field}`"] = json.dumps(cpe[field])

            relation = {
                'id': ID.get_id(),
                'cve': item['cve'],
                'cve_id': item['id'],
                'cpe_id': cpe['id'],
                'update_time': item['cve_last_modified_time'],
            }
            err = self.data.price_exists(field='id', price=relation['id'], table='nvd_cpe_relation')
            while err['error'] == 102:
                relation['id'] = ID.get_id()
                err = self.data.price_exists(field='id', price=relation['id'], table='nvd_cpe_relation')
            relationdata = {}
            for field in relation:
                if field == 'url' or "time" in field:
                    relationdata[f"`{field}`"] = relation[field]
                elif field == "id":
                    relationdata[f"`{field}`"] = str(relation[field])
                elif relation.get(field):
                    relationdata[f"`{field}`"] = json.dumps(relation[field])
            # 验证表结构是否存在
            if self.cpe <= 1:
                logger.error(self.data.field_exists(fields=cpe.keys(), table='nvd_cpe_all'))
                logger.error(self.data.field_exists(fields=relation.keys(), table='nvd_cpe_relation'))
                self.cpe += 1
            # 验证cpe是否存在表中
            err = self.data.price_exists(field='cpe', price=cpe['cpe'], table='nvd_cpe_all')
            # 不存在数据库，直接进行存储
            if err['error'] == 101:
                log = self.data.add_data(item=cpedata, table='nvd_cpe_all')
                logger.error(f'{item["cve"]} cpe_all数据表 {cpe["cpe"]}' + log)
                log = self.data.add_data(item=relationdata, table='nvd_cpe_relation')
                logger.error(f'{item["cve"]} cpe_relation数据表 {cpe["cpe"]}' + log)

            # 存在，获取cpeid与cve做关联
            elif err['error'] == 102:
                err_id = err['data'][0]
                # 存在数据，查看是否存在关联数据并删除
                cpe_relation = self.data.price_exists(field='cve', price=item['cve'], table='nvd_cpe_relation',
                                                      field2='cpe_id', price2=err_id)
                if cpe_relation['error'] == 102:
                    relation_id = cpe_relation['data'][0]
                    for i in relation_id:
                        log = self.data.delete_data(table='nvd_cpe_relation', field='id', price=i)
                        logger.error(f"{item['cve']} cpe_relation数据表：" + log)

                cpe_id = err['data'][0][0]
                relationdata['`cpe_id`'] = json.dumps(cpe_id)

                logger.error(f'{item["cve"]} cpe_all数据表 {cpe["cpe"]} 数据已存在，数据库id为{cpe_id}')
                log = self.data.add_data(item=relationdata, table='nvd_cpe_relation')
                logger.error(f'{item["cve"]} cpe_relation数据表 {cpe["cpe"]}' + log)
            else:
                logger.error(f'{item["cve"]} {cpe["cpe"]}数据查询失败：错误信息{err["log"]}')

    # 添加cvss3数据方法
    def add_cvss3(self, ID, item):
        # 向cvss3_all、cvss3表添加数据
        if self.cvss3 <= 1:
            logger.error(self.data.table_exists(table='nvd_cvss3_all'))
            logger.error(self.data.table_exists(table='nvd_cvss3'))

        # 判断cvss3数据是否存在，存在则删除
        err = self.data.price_exists(field='cve', price=item['cve'], table='nvd_cvss3_all')
        if err['error'] == 102:
            cvss3_id = err['data'][0]
            for i in cvss3_id:
                log = self.data.delete_data(table='nvd_cvss3_all', field='id', price=i)
                logger.error(f"{item['cve']} cvss3_all表数据" + log)
        # 判断cvss3_all数据是否存在，存在则删除
        err = self.data.price_exists(field='cve', price=item['cve'], table='nvd_cvss3')
        if err['error'] == 102:
            cvss3_id = err['data'][0]
            for i in cvss3_id:
                log = self.data.delete_data(table='nvd_cvss3', field='id', price=i)
                logger.error(f"{item['cve']} cvss3表数据" + log)

        cvss3_data_all = item['cvss3'] if item['cvss3'] else []

        for cvss3_data in cvss3_data_all:

            cvss3 = {'id': ID.get_id(), 'cve': item['cve'],
                     'vector_string': cvss3_data['cvssData']['vectorString'],
                     'attack_vector': cvss3_data['cvssData']['attackVector'],
                     'attack_complexity': cvss3_data['cvssData']['attackComplexity'],
                     'privilegeds_required': cvss3_data['cvssData']['privilegesRequired'],
                     'user_interaction': cvss3_data['cvssData']['userInteraction'],
                     'scope': cvss3_data['cvssData']['scope'],
                     'confidentiality_impact': cvss3_data['cvssData']['confidentialityImpact'],
                     'integrity_impact': cvss3_data['cvssData']['integrityImpact'],
                     'availability_impact': cvss3_data['cvssData']['availabilityImpact'],
                     'base_score': cvss3_data['cvssData']['baseScore'],
                     'base_severity': cvss3_data['cvssData']['baseSeverity'],
                     'exploitability_score': cvss3_data['exploitabilityScore'],
                     'impact_score': cvss3_data['impactScore'],
                     'create_time': item['create_time'],
                     'update_time': item['cve_last_modified_time'],
                     }
            if self.cvss3 <= 1:
                logger.error(self.data.field_exists(fields=cvss3.keys(), table='nvd_cvss3_all'))

            err = self.data.price_exists(field='id', price=cvss3['id'], table='nvd_cvss3_all')
            while err['error'] == 102:
                cvss3['id'] = ID.get_id()
                err = self.data.price_exists(field='id', price=cvss3['id'], table='nvd_cvss3_all')
            cvss3data = {}
            for field in cvss3:
                if field == 'url' or "time" in field:
                    cvss3data[f"`{field}`"] = cvss3[field]
                elif field == "id":
                    cvss3data[f"`{field}`"] = str(cvss3[field])
                elif cvss3.get(field):
                    cvss3data[f"`{field}`"] = json.dumps(cvss3[field])
            logger.error(f"{item['cve']} cvss3_all数据表" + self.data.add_data(item=cvss3data, table='nvd_cvss3_all'))

            cvss33 = {
                'id': ID.get_id(),
                'cve': item['cve'],
                'score': cvss3_data['cvssData']['baseScore'],
                'vector': cvss3_data['cvssData']['vectorString'],
            }
            if self.cvss3 <= 1:
                logger.error(self.data.field_exists(fields=cvss33.keys(), table='nvd_cvss3'))
                self.cvss3 += 1
            err = self.data.price_exists(field='id', price=cvss33['id'], table='nvd_cvss3')
            while err['error'] == 102:
                cvss33['id'] = ID.get_id()
                err = self.data.price_exists(field='id', price=cvss33['id'], table='nvd_cvss3')
            cvss3data = {}
            for field in cvss33:
                if field == 'url' or "time" in field:
                    cvss3data[f"`{field}`"] = cvss33[field]
                elif field == "id":
                    cvss3data[f"`{field}`"] = str(cvss33[field])
                elif cvss33.get(field):
                    cvss3data[f"`{field}`"] = json.dumps(cvss33[field])

            logger.error(f"{item['cve']} cvss3数据表" + self.data.add_data(item=cvss3data, table='nvd_cvss3'))

        if not cvss3_data_all:
            logger.error(f"{item['cve']} 无cvss3数据")

    # 添加cvss2数据方法
    def add_cvss2(self, ID, item):
        # 向cvss2_all、cvss2表添加数据
        if self.cvss2 <= 1:
            logger.error(self.data.table_exists(table='nvd_cvss2_all'))
            logger.error(self.data.table_exists(table='nvd_cvss2'))

        # 判断cvss2数据是否存在，存在则删除
        err = self.data.price_exists(field='cve', price=item['cve'], table='nvd_cvss2_all')
        if err['error'] == 102:
            cvss2_id = err['data'][0]
            for i in cvss2_id:
                log = self.data.delete_data(table='nvd_cvss2_all', field='id', price=i)
                logger.error(f"{item['cve']} cvss2_all表数据" + log)
        # 判断cvss2_all数据是否存在，存在则删除
        err = self.data.price_exists(field='cve', price=item['cve'], table='nvd_cvss2')
        if err['error'] == 102:
            cvss2_id = err['data'][0]
            for i in cvss2_id:
                log = self.data.delete_data(table='nvd_cvss2', field='id', price=i)
                logger.error(f"{item['cve']} cvss2表数据" + log)

        cvss2_data_all = item['cvss2'] if item['cvss2'] else []
        for cvss2_data in cvss2_data_all:

            cvss2 = {'id': ID.get_id(), 'cve': item['cve'],
                     'vector': cvss2_data['cvssData']['vectorString'],
                     'access_vector': cvss2_data['cvssData']['accessVector'],
                     'access_complexity': cvss2_data['cvssData']['accessComplexity'],
                     'authentication': cvss2_data['cvssData']['authentication'],
                     'confidentiality_impact': cvss2_data['cvssData']['confidentialityImpact'],
                     'integrity_impact': cvss2_data['cvssData']['integrityImpact'],
                     'availability_impact': cvss2_data['cvssData']['availabilityImpact'],
                     'exploitability_score': cvss2_data['exploitabilityScore'],
                     'impact_score': cvss2_data['impactScore'],
                     'ac_insuf_info': "1" if cvss2_data['acInsufInfo'] else "0",
                     'obtain_all_privilege': "1" if cvss2_data['obtainAllPrivilege'] else "0",
                     'obtain_user_privilege': "1" if cvss2_data['obtainUserPrivilege'] else "0",
                     'obtain_other_privilege': "1" if cvss2_data['obtainOtherPrivilege'] else "0",
                     'user_interaction_required': "1" if cvss2_data.get('userInteractionRequired', None) else "0",
                     'base_score': str(cvss2_data['cvssData']['baseScore']),
                     'severity': cvss2_data['baseSeverity'],
                     'create_time': item['create_time'],
                     'update_time': item['cve_last_modified_time'],
                     }
            if self.cvss2 <= 1:
                logger.error(self.data.field_exists(fields=cvss2.keys(), table='nvd_cvss2_all'))

            err = self.data.price_exists(field='id', price=cvss2['id'], table='nvd_cvss2_all')
            while err['error'] == 102:
                cvss2['id'] = ID.get_id()
                err = self.data.price_exists(field='id', price=cvss2['id'], table='nvd_cvss2_all')
            cvss2data = {}
            for field in cvss2:
                if field == 'url' or "time" in field:
                    cvss2data[f"`{field}`"] = cvss2[field]
                elif field == "id":
                    cvss2data[f"`{field}`"] = str(cvss2[field])
                elif cvss2.get(field):
                    cvss2data[f"`{field}`"] = json.dumps(cvss2[field])

            log = self.data.add_data(item=cvss2data, table='nvd_cvss2_all')
            logger.error(f"{item['cve']} cvss2_all数据表" + log)

            cvss22 = {
                'id': ID.get_id(),
                'cve': item['cve'],
                'score': str(cvss2_data['cvssData']['baseScore']),
                'vector': cvss2_data['cvssData']['vectorString'],
            }
            if self.cvss2 <= 1:
                logger.error(self.data.field_exists(fields=cvss22.keys(), table='nvd_cvss2'))
                self.cvss2 += 1
            err = self.data.price_exists(field='id', price=cvss22['id'], table='nvd_cvss2')
            while err['error'] == 102:
                cvss22['id'] = ID.get_id()
                err = self.data.price_exists(field='id', price=cvss22['id'], table='nvd_cvss2')
            cvss22data = {}
            for field in cvss22:
                if field == 'url' or "time" in field:
                    cvss22data[f"`{field}`"] = cvss22[field]
                elif field == "id":
                    cvss22data[f"`{field}`"] = str(cvss22[field])
                elif cvss22.get(field):
                    cvss22data[f"`{field}`"] = json.dumps(cvss22[field])
            log = self.data.add_data(item=cvss22data, table='nvd_cvss2')
            logger.error(f"{item['cve']} cvss2数据表" + log)

    # 数据校验功能
    def VerificationData(self, item):

        try:
            # 校验数据是否存在数据库
            err = self.data.price_exists(field='cve', price=item['cve'], table='nvd')
            # 不存在数据库，直接进行存储
            if err['error'] == 101:
                return item
            # 查询语句出错，返回信息，停止程序
            elif err['error'] == 104 or err['error'] == 103:
                logger.error(f'{item["cve"]}数据查询失败：错误信息{err["log"]}')
            # 查询数据库中已有数据的数据更新时间
            data_stime = \
                self.data.query_page(field=item['cve'], name='cve_last_modified_time', fields='cve', table='nvd')[
                    0]
            # 没有数据更新时间，再次进行存储
            if not data_stime:
                data_id = err['data'][0]
                for i in data_id:
                    log = self.data.delete_data(table='nvd', field='id', price=i)
                    logger.error(f"{item['cve']} nvd表数据" + log)
                logger.error(f'{item["cve"]}数据存在,但无更新日期，进行更新')
                return item
            # 存在更新时间与当前爬取到时间比较，是否需要数据存储
            date_obj = datetime.datetime.strptime(item['cve_last_modified_time'].strftime('%Y-%m-%d %H:%M:%S'),
                                                  "%Y-%m-%d %H:%M:%S")

            # 有新的更新时间进行数据存储
            if data_stime < date_obj:
                data_id = err['data'][0]
                for i in data_id:
                    log = self.data.delete_data(table='nvd', field='id', price=i)
                    logger.error(f"{item['cve']} nvd表数据" + log)
                logger.error(f'更新{item["cve"]}数据')
                return item

        except Exception as e:
            logger.error(f"数据库校验数据失败，错误信息{e}")

    # 爬虫程序执行到最后
    def close_spider(self, spider):
        try:
            logger.error(f"数据总量为{spider.data_max},共有{spider.max}条详情页无数据")
            data_max = self.data.disconnect(time='create_time')
            logger.error(f"程序执行数据实例化存储{data_max}")
        except:
            logger.error(f'关闭程序异常')
