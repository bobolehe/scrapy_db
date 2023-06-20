import scrapy
from metasploit import settings


class MetasSpider(scrapy.Spider):
    name = "metas"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://www.rapid7.com/db/?q=&type=metasploit&page=1"]
    url1 = 'https://www.rapid7.com'
    url2 = "https://www.rapid7.com/db/?q=&type=metasploit&page=%d"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.MYSQL_HOST = kwargs.get('host') if kwargs.get('host') else settings.MYSQL_HOST
        settings.MYSQL_USER = kwargs.get('user') if kwargs.get('user') else settings.MYSQL_USER
        settings.MYSQL_PWD = kwargs.get('pwd') if kwargs.get('pwd') else settings.MYSQL_PWD
        settings.MYSQL_PORT = kwargs.get('port') if kwargs.get('port') else settings.MYSQL_PORT
        settings.MYSQL_DB = kwargs.get('db') if kwargs.get('db') else settings.MYSQL_DB
        settings.MYSQL_TB = kwargs.get('tb') if kwargs.get('tb') else settings.MYSQL_TB
        self.page_max = int(kwargs.get('page')) if kwargs.get('page') else int(0)
        self.page = int(0)

    def parse(self, response):
        # .extract_first()
        # 提取详情页所有的a标签
        a_list = response.xpath('/html/body//div[@class="pageContent vulndb"]//section[@class="vulndb__results"]/a')
        for a in a_list:
            # 提取a标签中的url、title、Disclosed字段
            url = a.xpath('./@href').extract_first()
            title = str(a.xpath('.//div[@class="resultblock__info-title"]/text()').extract_first()).strip()
            meta = str(a.xpath('.//div[@class="resultblock__info-meta"]/text()').extract_first()).strip()
            meta = self.datestime(meta.replace('Disclosed: ', ""))
            print(url, title, meta)

        # 判断是否有指定页数参数
        if self.page_max:
            self.page += 1
            if self.page <= self.page_max:
                url = format(self.url2 % self.page)
                yield scrapy.Request(url=url, callback=self.data_spider, dont_filter=True)
        else:
            # 获取下一页
            page_xiayiye = response.xpath(
                '/html/body//div[@class="pageContent vulndb"]//section[@class="vulndb__results"]/div//ul/li[@class="active"]/following-sibling::li[1]/a/@href').extract_first()
            print(page_xiayiye)

    def data_spider(self, response):
        pass

    def datestime(self, stime):
        """
        简单翻译爬取到的英语月份
        :param self:
        :param stime:
        :return:
        """
        date1 = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
        }
        date2 = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }

        stime = stime
        stime = stime.replace(',', '').split(' ')

        stime[0] = str(date2[stime[0]])
        stime = [stime[2], stime[0], stime[1]]
        return '-'.join(stime)
