# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SnykcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    # 漏洞类型
    Vulnerability = scrapy.Field()
    # 类型
    Type = scrapy.Field()
    # 发布日期
    INTRODUCED_stime = scrapy.Field()
    # 影响到的软件包
    Affecting = scrapy.Field()
    # 影响到的版本
    Version = scrapy.Field()
    # 漏洞详情页链接
    url = scrapy.Field()
    # 漏洞详情页需要二次跳转链接
    second_url = scrapy.Field()
    # 详情页中cve、cwe参数
    CVE = scrapy.Field()
    CWE = scrapy.Field()
    # How to fix内容
    MarkdownSection = scrapy.Field()
    # Overview 内容
    Overview = scrapy.Field()
    # References 内容
    ReferencesData = scrapy.Field()
    # synk CVSS数据
    SnykCVSS = scrapy.Field()
    # Redhat数据
    RedHat = scrapy.Field()
    # Details数据
    Details = scrapy.Field()
    # 下沉一次获取数据
    sink_one_data = scrapy.Field()
    # 下沉两次获取数据
    sink_two_data = scrapy.Field()
    # 数据获取时间
    stime = scrapy.Field()

