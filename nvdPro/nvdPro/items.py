# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NvdproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    cve = scrapy.Field()
    description = scrapy.Field()
    cve_published_time = scrapy.Field()
    cve_last_modified_time = scrapy.Field()
    hyper = scrapy.Field()
    cwe = scrapy.Field()
    cpe = scrapy.Field()
    cvss2 = scrapy.Field()
    cvss3 = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    last_modified_time = scrapy.Field()
    update_num = scrapy.Field()


