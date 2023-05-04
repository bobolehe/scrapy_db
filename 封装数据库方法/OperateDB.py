import mysql.connector
import re
import datetime


class MysqlData:
    def __init__(self):
        self.db = None
        self.cursor = None
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
            self.db = mysql.connector.connect(host=host, user=user, password=password, port=port)
            self.cursor = self.db.cursor()
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
                'cursor': self.cursor,
                'db': self.db
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
            self.cursor.execute(sql)
            self.db.commit()
        except:
            # 失败回滚，返回失败信息
            self.db.rollback()
            return f"判断数据库{data}是否存在失败"
        else:
            # 数据库存在无需创建
            self.cursor.execute(f'use {data};')
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
            self.cursor.execute(sql)
            tables = self.cursor.fetchall()
        except:
            return "查询数据库表结构失败"
        else:
            # 解析查询到的数据库表
            tables_list = re.findall('(\'.*?\')', str(tables))
            tables_list = [re.sub("'", '', each) for each in tables_list]

        # 判断指定表名是否存在其中
        if table in tables_list:
            fields = {'url': {}, 'stime': {}}
            return self.field_exists(fields=fields)
        else:
            # 创建表结构
            try:
                sql = f"""CREATE TABLE {table}  (
                              `id` int(0) NOT NULL AUTO_INCREMENT,
                              `url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                              `stime` datetime(0) NOT NULL,
                              PRIMARY KEY (`id`) USING BTREE
                            ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
                            """
                self.cursor.execute(sql)
                self.db.commit()
                return f"数据表{table}不存在进行创建表结构成功"
            except:
                self.db.rollback()
                return f"数据表{table}不存在进行创建表结构失败,请提供正确的spl语句"

    def disconnect(self):
        """
        关闭提供的链接以及游标
        :return: 返回提示信息
        """
        try:
            sql = f"SELECT * FROM {self.table} WHERE stime >= '{self.ks_time}';"
            # sql = "SELECT * FROM eol WHERE stime >= '2023-04-11 17:16:10';"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except:
            self.cursor.close()
            self.db.close()
            return '查询失败'
        else:
            self.cursor.close()
            self.db.close()
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
                elif k == 'stime':
                    sql_new = sql + f"ADD COLUMN `{k}` datetime(255) NULL ON UPDATE CURRENT_TIMESTAMP(255) AFTER `{field}`;"
                else:
                    sql_new = sql + f"ADD COLUMN `{k}` json NULL AFTER `{field}`;"
                self.cursor.execute(sql_new)
                self.db.commit()
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
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
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
            self.cursor.execute(sql, tuple(values))
            self.db.commit()
        except:
            return '数据实例化存储失败'
        else:
            return '数据实例化存储成功'

    def price_exists(self, field=str(), price=None):
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

        sql = f"select url from {self.table} where {field}='{price}';"

        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except:
            err = {
                'error': 104,
                'log': f'{sql}输出查询失败'
            }
            return err
        else:
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


if __name__ == '__main__':
    data = MysqlData()
    retu = data.connect_data()
    if retu.get('db'):
        # 连接成功数据库，进入数据库和查看表结构
        print(data.data_exists(data='spiders'))
        print(data.table_exists(table='attgroups'))
        # 测试item数据
        item = {'Associated_Group_Descriptions': '[{"name": "Comment Crew", "Description": '
                                                 '"[1]https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                                 '{"name": "Comment Group", "Description": '
                                                 '"[1]https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                                 '{"name": "Comment Panda", "Description": '
                                                 '"[2]http://cdn0.vox-cdn.com/assets/4589853/crowdstrike-intelligence-report-putter-panda.original.pdf"}]',
                'Associated_Groups': '"Comment Crew, Comment Group, Comment Panda"',
                'Created': '"31 May 2017"',
                'Last_Modified': '"26 May 2021"',
                'Software': '[{"ID": "S0017", "Name": "BISCUIT", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "Command and Scripting InterpreterWindows Command '
                            'ShellEncrypted ChannelAsymmetric CryptographyFallback '
                            'ChannelsIngress Tool TransferInput CaptureKeyloggingProcess '
                            'DiscoveryScreen CaptureSystem Information DiscoverySystem '
                            'Owner/User Discovery"}, {"ID": "S0119", "Name": "Cachedump", '
                            '"References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "OS Credential DumpingCached Domain Credentials"}, '
                            '{"ID": "S0025", "Name": "CALENDAR", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "Command and Scripting InterpreterWindows Command '
                            'ShellWeb ServiceBidirectional Communication"}, {"ID": "S0026", '
                            '"Name": "GLOOXMAIL", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "Web ServiceBidirectional Communication"}, {"ID": '
                            '"S0008", "Name": "gsecdump", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "OS Credential DumpingLSA SecretsOS Credential '
                            'DumpingSecurity Account Manager"}, {"ID": "S0100", "Name": '
                            '"ipconfig", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "System Network Configuration Discovery"}, {"ID": '
                            '"S0121", "Name": "Lslsass", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "OS Credential DumpingLSASS Memory"}, {"ID": '
                            '"S0002", "Name": "Mimikatz", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "Access Token ManipulationSID-History '
                            'InjectionAccount ManipulationBoot or Logon Autostart '
                            'ExecutionSecurity Support ProviderCredentials from Password '
                            'StoresCredentials from Web BrowsersCredentials from Password '
                            'StoresCredentials from Password StoresWindows Credential '
                            'ManagerOS Credential DumpingLSASS MemoryOS Credential '
                            'DumpingSecurity Account ManagerOS Credential DumpingLSA '
                            'SecretsOS Credential DumpingDCSyncRogue Domain ControllerSteal '
                            'or Forge Authentication CertificatesSteal or Forge Kerberos '
                            'TicketsGolden TicketSteal or Forge Kerberos TicketsSilver '
                            'TicketUnsecured CredentialsPrivate KeysUse Alternate '
                            'Authentication MaterialPass the TicketUse Alternate '
                            'Authentication MaterialPass the Hash"}, {"ID": "S0039", "Name": '
                            '"Net", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "Account DiscoveryDomain AccountAccount '
                            'DiscoveryLocal AccountCreate AccountDomain AccountCreate '
                            'AccountLocal AccountIndicator RemovalNetwork Share Connection '
                            'RemovalNetwork Share DiscoveryPassword Policy '
                            'DiscoveryPermission Groups DiscoveryLocal GroupsPermission '
                            'Groups DiscoveryDomain GroupsRemote ServicesSMB/Windows Admin '
                            'SharesRemote System DiscoverySystem Network Connections '
                            'DiscoverySystem Service DiscoverySystem ServicesService '
                            'ExecutionSystem Time Discovery"}, {"ID": "S0122", "Name": '
                            '"Pass-The-Hash Toolkit", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "Use Alternate Authentication MaterialPass the '
                            'Hash"}, {"ID": "S0012", "Name": "PoisonIvy", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "Application Window DiscoveryBoot or Logon '
                            'Autostart ExecutionActive SetupBoot or Logon Autostart '
                            'ExecutionRegistry Run Keys / Startup FolderCommand and Scripting '
                            'InterpreterWindows Command ShellCreate or Modify System '
                            'ProcessWindows ServiceData from Local SystemData StagedLocal '
                            'Data StagingEncrypted ChannelSymmetric CryptographyIngress Tool '
                            'TransferInput CaptureKeyloggingModify RegistryObfuscated Files '
                            'or InformationProcess InjectionDynamic-link Library '
                            'InjectionRootkit"}, {"ID": "S0029", "Name": "PsExec", '
                            '"References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "Create AccountDomain AccountCreate or Modify '
                            'System ProcessWindows ServiceLateral Tool TransferRemote '
                            'ServicesSMB/Windows Admin SharesSystem ServicesService '
                            'Execution"}, {"ID": "S0006", "Name": "pwdump", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "OS Credential DumpingSecurity Account Manager"}, '
                            '{"ID": "S0345", "Name": "Seasalt", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report-appendix.zip", '
                            '"https://www.mcafee.com/enterprise/en-us/assets/reports/rp-operation-oceansalt.pdf"], '
                            '"Techniques": "Application Layer ProtocolWeb ProtocolsBoot or '
                            'Logon Autostart ExecutionRegistry Run Keys / Startup '
                            'FolderCommand and Scripting InterpreterWindows Command '
                            'ShellCreate or Modify System ProcessWindows ServiceFile and '
                            'Directory DiscoveryIndicator RemovalFile DeletionIngress Tool '
                            'TransferMasqueradingMasquerade Task or ServiceObfuscated Files '
                            'or InformationProcess Discovery"}, {"ID": "S0057", "Name": '
                            '"Tasklist", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "Process DiscoverySoftware DiscoverySecurity '
                            'Software DiscoverySystem Service Discovery"}, {"ID": "S0109", '
                            '"Name": "WEBC2", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"], '
                            '"Techniques": "Command and Scripting InterpreterWindows Command '
                            'ShellHijack Execution FlowDLL Search Order HijackingIngress Tool '
                            'Transfer"}, {"ID": "S0123", "Name": "xCmd", "References": '
                            '["https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report-appendix.zip"], '
                            '"Techniques": "System ServicesService Execution"}]',
                'Techniques_Used': '[{"Domain": "Enterprise", "id": "T1087.001", "Name": '
                                   '"Account Discovery: Local Account", "Use": "APT1 used the '
                                   'commands net localgroup,net user, and net group to find '
                                   'accounts on the '
                                   'system.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1583.001", "Name": '
                                   '"Acquire Infrastructure: Domains", "Use": "APT1 has '
                                   'registered hundreds of domains for use in '
                                   'operations.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1560.001", "Name": '
                                   '"Archive Collected Data: Archive via Utility", "Use": '
                                   '"APT1 has used RAR to compress files before moving them '
                                   'outside of the victim '
                                   'network.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1119", "Name": '
                                   '"Automated Collection", "Use": "APT1 used a batch script '
                                   'to perform a series of discovery techniques and saves it '
                                   'to a text '
                                   'file.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1059.003", "Name": '
                                   '"Command and Scripting Interpreter: Windows Command '
                                   'Shell", "Use": "APT1 has used the Windows command shell '
                                   'to execute commands, and batch scripting to automate '
                                   'execution.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1584.001", "Name": '
                                   '"Compromise Infrastructure: Domains", "Use": "APT1 '
                                   'hijacked FQDNs associated with legitimate websites hosted '
                                   'by hop '
                                   'points.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1005", "Name": "Data '
                                   'from Local System", "Use": "APT1 has collected files from '
                                   'a local '
                                   'victim.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1114.001", "Name": '
                                   '"Email Collection: Local Email Collection", "Use": "APT1 '
                                   'uses two utilities, GETMAIL and MAPIGET, to steal email. '
                                   'GETMAIL extracts emails from archived Outlook .pst '
                                   'files.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1114.002", "Name": '
                                   '"Email Collection: Remote Email Collection", "Use": "APT1 '
                                   'uses two utilities, GETMAIL and MAPIGET, to steal email. '
                                   'MAPIGET steals email still on Exchange servers that has '
                                   'not yet been '
                                   'archived.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1585.002", "Name": '
                                   '"Establish Accounts: Email Accounts", "Use": "APT1 has '
                                   'created email accounts for later use in social '
                                   'engineering, phishing, and when registering '
                                   'domains.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1036.005", "Name": '
                                   '"Masquerading: Match Legitimate Name or Location", "Use": '
                                   '"The file name AcroRD32.exe, a legitimate process name '
                                   "for Adobe's Acrobat Reader, was used by APT1 as a name "
                                   'for '
                                   'malware.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdfhttps://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report-appendix.zip"}, '
                                   '{"Domain": "Enterprise", "id": "T1135", "Name": "Network '
                                   'Share Discovery", "Use": "APT1 listed connected network '
                                   'shares.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1588.001", "Name": '
                                   '"Obtain Capabilities: Malware", "Use": "APT1 used '
                                   'publicly available malware for privilege '
                                   'escalation.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1588.002", "Name": '
                                   '"Obtain Capabilities: Tool", "Use": "APT1 has used '
                                   'various open-source tools for privilege escalation '
                                   'purposes.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1003.001", "Name": "OS '
                                   'Credential Dumping: LSASS Memory", "Use": "APT1 has been '
                                   'known to use credential dumping using '
                                   'Mimikatz.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1566.001", "Name": '
                                   '"Phishing: Spearphishing Attachment", "Use": "APT1 has '
                                   'sent spearphishing emails containing malicious '
                                   'attachments.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1566.002", "Name": '
                                   '"Phishing: Spearphishing Link", "Use": "APT1 has sent '
                                   'spearphishing emails containing hyperlinks to malicious '
                                   'files.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1057", "Name": "Process '
                                   'Discovery", "Use": "APT1 gathered a list of running '
                                   'processes on the system using tasklist '
                                   '/v.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1021.001", "Name": '
                                   '"Remote Services: Remote Desktop Protocol", "Use": "The '
                                   'APT1 group is known to have used RDP during '
                                   'operations.https://www.fireeye.com/blog/threat-research/2014/05/the-pla-and-the-800am-500pm-work-day-fireeye-confirms-dojs-findings-on-apt1-intrusion-activity.html"}, '
                                   '{"Domain": "Enterprise", "id": "T1016", "Name": "System '
                                   'Network Configuration Discovery", "Use": "APT1 used the '
                                   'ipconfig /all command to gather network configuration '
                                   'information.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1049", "Name": "System '
                                   'Network Connections Discovery", "Use": "APT1 used the net '
                                   'use command to get a listing on network '
                                   'connections.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1007", "Name": "System '
                                   'Service Discovery", "Use": "APT1 used the commands net '
                                   'start and tasklist to get a listing of the services on '
                                   'the '
                                   'system.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}, '
                                   '{"Domain": "Enterprise", "id": "T1550.002", "Name": "Use '
                                   'Alternate Authentication Material: Pass the Hash", "Use": '
                                   '"The APT1 group is known to have used pass the '
                                   'hash.https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"}]',
                'description_body': '"APT1 is a Chinese threat group that has been attributed '
                                    'to the 2nd Bureau of the People\\u2019s Liberation Army '
                                    '(PLA) General Staff Department\\u2019s (GSD) 3rd '
                                    'Department, commonly known by its Military Unit Cover '
                                    'Designator (MUCD) as Unit 61398. "',
                'name': '"APT1"',
                'stime': '2023-05-04 15:34:22.525797',
                'title_id': '"G0006"',
                'url': 'https://attack.mitre.org/groups/G0006/'}
        # 数据库和数据表存在或创建完成后,传入item对象，创建剩余的字段结构
        print(data.field_exists(fields=item))
        # 添加测试数据
        print(data.add_data(item=item))
        # 关闭数据库
        print(data.disconnect())
