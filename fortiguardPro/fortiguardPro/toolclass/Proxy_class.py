import random
import settings
from proxy_module import GetProxy


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

    PROXY_https = settings.PROXY_HTTPS

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

        # # 设置代理
        request.meta['http_proxy'] = 'https://' + random.choice(settings.PROXY_HTTPS)

        return None

    # 异常拦截
    def process_exception(self, request, exception, spider):

        h = GetProxy()
        settings.PROXY_https = h.proxies_data()

        if request.url.split(':')[0] == 'http':
            request.headers['User-Agent'] = random.choice(self.user_agent_list)
            request.meta['http_proxy'] = 'http://' + random.choice(settings.PROXY_https)
        else:
            request.headers['User-Agent'] = random.choice(self.user_agent_list)
            request.meta['http_proxy'] = 'https://' + random.choice(settings.PROXY_https)

        return request  # 修改请求信息后重新发送请求

    # 日志方法
    def spider_opened(self, spider):

        spider.logger.info('Spider opened: %s' % spider.name)
