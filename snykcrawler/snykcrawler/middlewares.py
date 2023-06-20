# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import time
import re
import logging
from scrapy import signals
from scrapy.http import HtmlResponse
from snykcrawler import settings
from snykcrawler.toolclass.proxy_module import GetProxy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

# 实例化日志类
logger = logging.getLogger(__name__)


class SnykcrawlerSpiderMiddleware:
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


class SnykcrawlerDownloaderMiddleware:
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
    PROXY_http = settings.PROXY_HTTPS

    PROXY_https = settings.PROXY_HTTPS

    # 请求拦截
    def process_request(self, request, spider):
        # # UA伪装
        request.headers['User-Agent'] = random.choice(self.user_agent_list)

        # # 设置代理
        request.meta['http_proxy'] = 'https://' + random.choice(settings.PROXY_HTTPS)
        # print(f'使用代理{request.meta["http_proxy"]}')
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

    # 响应拦截
    def process_response(self, request, response, spider):
        pattern = r'https://security\.snyk\.io/vuln/.*$'
        pattern2 = r'https://security\.snyk\.io/vuln/(\d+)'
        try:
            # 正则匹配文章详情页，实现动态加载数据
            if re.match(pattern, request.url):
                if re.match(pattern2, request.url):
                    return response
                print('动态加载')
                chrome_options = Options()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--headless')
                bro = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)
                bro.get(request.url)
                cvss = bro.find_elements_by_xpath(
                    '//*[@id="__layout"]/div/main//div[@class="details-box__body"]/div/button')
                if cvss:
                    cvss[0].click()

                db = bro.find_elements_by_xpath(
                    '//*[@id="__layout"]/div/main//div[@class="vue--block-expandable__text"]')
                for i in db:
                    if i.text == "Red Hat":
                        i.click()
                time.sleep(3)
                page_text = bro.page_source
                bro.quit()
                new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
                return new_response
            return response
        except:
            logger.error(f'{request.url}获取详细页源码失败')

    # 日志方法
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)