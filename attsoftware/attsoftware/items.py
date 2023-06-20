# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AttsoftwareItem(scrapy.Item):
    # define the fields for your item here like:
    stime = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    card = scrapy.Field()
    description_body = scrapy.Field()
    Techniques = scrapy.Field()
    Software = scrapy.Field()
    software_id = scrapy.Field()
    uptodate_time = scrapy.Field()
    pagemax = scrapy.Field()
