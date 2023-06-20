# Scrapy settings for cxsecurity project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "cxsecurity"

SPIDER_MODULES = ["cxsecurity.spiders"]
NEWSPIDER_MODULE = "cxsecurity.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "cxsecurity (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "cxsecurity.middlewares.CxsecuritySpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "cxsecurity.middlewares.IPSproDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "cxsecurity.pipelines.DataPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# 配置项
# 忽略对证书验证的严格检查
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# 请求头
# USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
# USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
HTTPERROR_ALLOWED_CODES = [404, 403, 401]
# 访问延迟时间
RANDOM_DELAY = 10
# 访问重试次数
RETRY_TIMES = 3
# 重定向
REDIRECT_ENABLED = False
REDIRECT_MAX_TIMES = 10
# 智能限速
# AUTOTHROTTLE_ENABLED = True
# 自动限速的初始延迟时间
# AUTOTHROTTLE_START_DELAY = 3
# # 下载延迟时间
# DOWNLOAD_DELAY = 6
# # 自动限速最大延迟时间
# AUTOTHROTTLE_MAX_DELAY = 30
# 下载器总共最大处理的并发请求数,默认值16
# CONCURRENT_REQUESTS = 1
# 单线程模式
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1
DOWNLOAD_DELAY = 10  # 设置请求间隔，以避免过于频繁的请求

# 终端接收信息
# LOG_LEVEL = 'ERROR'
# LOG_FILE = './log.log'

# mysql配置信息
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PWD = "123456"
MYSQL_PORT = 3306
MYSQL_DB = "spider"
MYSQL_TB = 'cxsecruity'

# 代理配置信息
PROXY_HTTPS = []

# 爬虫数据量
PAGE_MAX = 30