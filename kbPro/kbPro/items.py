# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KbproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    Updated_time = scrapy.Field()
    title = scrapy.Field()
    Overview = scrapy.Field()
    Description = scrapy.Field()
    Impact = scrapy.Field()
    Solution = scrapy.Field()
    # References字段
    Referenc = scrapy.Field()
    OtherInformation = scrapy.Field()
    stime = scrapy.Field()
    CCid = scrapy.Field()
    PageMax = scrapy.Field()
