# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EndoflifeproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    table_title = scrapy.Field()
    table_data = scrapy.Field()
    version = scrapy.Field()
    stime = scrapy.Field()
    datatime = scrapy.Field()
    pagemax = scrapy.Field()
