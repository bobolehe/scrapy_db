# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CoresecurityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    Description = scrapy.Field()
    vulnerabilty = scrapy.Field()
    category = scrapy.Field()
    platform = scrapy.Field()
    datamax = scrapy.Field()
    update_time = scrapy.Field()
    stime = scrapy.Field()

