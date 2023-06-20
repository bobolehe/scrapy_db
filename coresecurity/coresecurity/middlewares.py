# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import time
import logging

from scrapy import signals
from scrapy.http import HtmlResponse
from coresecurity import settings
from coresecurity.toolclass.proxy_module import GetProxy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

# 实例化日志类
logger = logging.getLogger(__name__)


class CoresecuritySpiderMiddleware:
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


class CoresecurityDownloaderMiddleware:
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
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 "
        "Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 "
        "Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
    # 代理ip
    PROXY_http = settings.PROXY_HTTPS

    PROXY_https = settings.PROXY_HTTPS

    # 请求拦截
    def process_request(self, request, spider):
        chrome_options = Options()
        # 关闭权限启动
        chrome_options.add_argument('--no-sandbox')
        # 禁用gpu加速
        chrome_options.add_argument("--disable-gpu")
        # 禁用浏览器正在被自动化程序控制的提示
        chrome_options.add_argument('--disable-infobars')
        # 配置对象添加替换User-Agent的命令
        chrome_options.add_argument('--user-agent=Mozilla/5.0 HAHA')
        # 无头模式
        chrome_options.add_argument('--headless')
        bro = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)

        repeat = 0
        timeout = 40
        while repeat < 5:
            try:
                bro.get(request.url)
                element = WebDriverWait(bro, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="block-coresecurity-content"]')))
                page_text = bro.page_source
                new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
                return new_response
            except:
                repeat += 1
                timeout += 10
                if repeat == 5:
                    logger.error(f'{request.url}获取详细页源码失败')
                logger.error(f'{request.url}获取详细页源码重新获取')
        return None

    # 异常拦截
    def process_exception(self, request, exception, spider):

        h = GetProxy()
        settings.PROXY_https = h.proxies_data()
        # print("切换代理池")
        if request.url.split(':')[0] == 'http':
            request.headers['User-Agent'] = random.choice(self.user_agent_list)
            request.meta['http_proxy'] = 'http://' + random.choice(settings.PROXY_https)
        else:
            request.headers['User-Agent'] = random.choice(self.user_agent_list)
            request.meta['http_proxy'] = 'https://' + random.choice(settings.PROXY_https)
        # print(f'使用代理{request.meta["http_proxy"]}')
        return request  # 修改请求信息后重新发送请求

    # def process_response(self, request, response, spider):
    #
    #     try:
    #         chrome_options = Options()
    #         chrome_options.add_argument('--no-sandbox')
    #         chrome_options.add_argument('--headless')
    #         driver = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)
    #         bro = WebDriverWait(driver, 30)
    #         driver.get(request.url)
    #         time.sleep(5)
    #         page_text = driver.page_source
    #         driver.quit()
    #         new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
    #         return new_response
    #     except:
    #         logger.error(f'{request.url}获取详细页源码失败')

    # 日志方法
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
