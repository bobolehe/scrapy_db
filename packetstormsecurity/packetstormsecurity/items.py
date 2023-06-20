# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PacketstormsecurityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    advisories = scrapy.Field()
    url = scrapy.Field()
    tags = scrapy.Field()
    detail = scrapy.Field()
    spider_max = scrapy.Field()

    stime = scrapy.Field()
    data_time = scrapy.Field()

