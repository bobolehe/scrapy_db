# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EolproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    product = scrapy.Field()
    EOLD = scrapy.Field()
    EOSL = scrapy.Field()
    Manu = scrapy.Field()
    Cate = scrapy.Field()
    Mode = scrapy.Field()
    Stat = scrapy.Field()
    stime = scrapy.Field()
    PageMax = scrapy.Field()
    dataPage = scrapy.Field()


