# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CxsecurityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    published_time = scrapy.Field()
    risk = scrapy.Field()
    local = scrapy.Field()
    remote = scrapy.Field()
    cve = scrapy.Field()
    cwe = scrapy.Field()
    stime = scrapy.Field()
    datamax = scrapy.Field()

