# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FortiguardproItem(scrapy.Item):
    # define the fields for your item here like:
    # 规则名称
    rule_name = scrapy.Field()
    # 规则发布时间
    rule_time = scrapy.Field()
    # 规则详情页
    url = scrapy.Field()
    # 规则 id
    rule_id = scrapy.Field()
    # 规则详情页名称
    rule_title = scrapy.Field()
    # Recommend_actions字段
    Recommend_actions = scrapy.Field()
    # CVE_References字段
    CVE_References = scrapy.Field()
    # Other_References字段
    Other_References = scrapy.Field()
    # 数据存储时间
    stime = scrapy.Field()
    # 规则详情页更新日期
    UpdatedStime = scrapy.Field()
    # 数据更新次数
    datamax = scrapy.Field()

