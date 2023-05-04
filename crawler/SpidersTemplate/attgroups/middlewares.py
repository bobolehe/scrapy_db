# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class AttgroupsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AttgroupsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class IPSproDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    # 伪装请求头列表
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    ]
    # 代理ip
    PROXY_http = [
        '223.70.126.84:3128',
        '47.57.188.208:80',
        '47.92.113.71:80'
    ]

    PROXY_https = ['221.201.198.108:64256', '42.54.92.204:64256',
                   '123.115.203.170:64256', '49.89.69.83:64256', '175.174.180.249:64256',
                   '113.237.230.120:64256', '124.116.112.35:64256', '202.110.28.32:64256', '27.156.194.204:64256',
                   '115.234.255.228:64256', '110.90.137.202:64256', '183.95.123.118:64256', '49.71.118.136:64256',
                   '114.99.6.193:64256', '124.94.184.27:64256', '122.246.88.9:64256', '119.112.192.23:64256',
                   '175.149.62.21:64256', '60.173.46.90:64256', '125.78.12.119:64256', '27.150.87.86:64256',
                   '180.108.37.135:64256', '42.177.101.171:64256', '60.167.90.254:64256', '123.244.154.109:64256',
                   '113.138.146.68:64256', '119.49.210.49:64256', '113.237.245.1:64256', '14.157.100.104:64256',
                   '115.234.200.140:64256', '115.239.103.11:64256', '59.59.214.13:64256', '115.152.211.134:64256',
                   '111.127.99.192:64256', '123.245.248.212:64256', '223.240.208.245:64256', '222.190.198.43:64256',
                   '122.6.91.200:64256', '117.37.130.4:64256', '125.87.83.153:64256', '113.138.146.63:64256',
                   '61.154.91.5:64256', '115.206.190.147:64256', '117.95.106.238:64256', '119.49.209.106:64256',
                   '113.231.38.44:64256', '114.106.146.182:64256', '117.26.193.107:64256', '119.183.73.37:64256',
                   '113.231.37.56:64256', '114.99.131.254:64256', '1.82.106.82:64256', '42.84.86.43:64256',
                   '113.141.222.225:64256', '42.56.3.204:64256', '119.129.252.33:64256', '175.170.40.94:64256',
                   '117.32.79.156:64256', '115.234.250.50:64256', '114.99.10.68:64256', '182.37.98.89:64256',
                   '59.58.148.21:64256', '113.231.82.15:64256', '113.241.138.8:64256', '117.34.230.85:64256',
                   '42.59.165.206:64256', '117.95.100.59:64256', '115.239.16.22:64256', '119.112.204.75:64256',
                   '117.34.230.148:64256', '115.204.62.148:64256', '36.42.102.98:64256', '49.84.136.26:64256',
                   '116.208.49.99:64256', '113.237.187.137:64256', '180.120.92.71:64256', '1.195.218.184:64256',
                   '42.84.91.169:64256', '114.103.89.231:64256', '119.49.209.188:64256', '113.138.147.144:64256',
                   '49.82.26.153:64256', '122.188.193.119:64256', '49.85.179.107:64256', '218.6.106.218:64256',
                   '27.37.249.202:64256', '222.90.3.95:64256', '180.109.49.43:64256', '125.87.82.27:64256',
                   '1.49.229.7:64256', '116.26.4.57:64256', '59.60.153.68:64256', '49.85.97.179:64256',
                   '123.96.186.107:64256', '117.64.248.206:64256', '222.246.229.29:64256', '115.198.75.207:64256',
                   '39.72.154.233:64256', '219.145.13.163:64256', '36.6.146.153:64256', '219.145.13.253:64256',
                   '114.106.146.42:64256', '110.88.30.117:64256', '180.126.192.97:64256', '140.237.144.246:64256',
                   '117.28.33.39:64256']

    # 请求拦截
    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # # UA伪装
        request.headers['User-Agent'] = random.choice(self.user_agent_list)
        # #
        # # 设置代理
        request.meta['http_proxy'] = 'https://' + random.choice(self.PROXY_https)
        print(request.meta['http_proxy'])
        return None

    # 异常拦截
    def process_exception(self, request, exception, spider):

        if request.url.split(':')[0] == 'http':
            request.headers['User-Agent'] = random.choice(self.user_agent_list)
            request.meta['http_proxy'] = 'http://' + random.choice(self.PROXY_http)
        else:
            request.headers['User-Agent'] = random.choice(self.user_agent_list)
            request.meta['http_proxy'] = 'https://' + random.choice(self.PROXY_https)
            print(request.meta['http_proxy'])
        return request  # 修改请求信息后重新发送请求

    # 日志方法
    def spider_opened(self, spider):
        print(spider.name)
        spider.logger.info('Spider opened: %s' % spider.name)
