# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CveprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    url = scrapy.Field()
    cve_id = scrapy.Field()
    cve_state = scrapy.Field()
    data_type = scrapy.Field()
    data_format = scrapy.Field()
    data_version = scrapy.Field()
    cve_data_meta = scrapy.Field()
    affects = scrapy.Field()
    problemtype = scrapy.Field()
    references = scrapy.Field()
    description = scrapy.Field()
    credits = scrapy.Field()
    generator = scrapy.Field()
    impact = scrapy.Field()
    solution = scrapy.Field()
    source = scrapy.Field()
    work_around = scrapy.Field()
    credit = scrapy.Field()
    exploit = scrapy.Field()
    timeline = scrapy.Field()
    configuration = scrapy.Field()
    data_update_time = scrapy.Field()
    data_time = scrapy.Field()


