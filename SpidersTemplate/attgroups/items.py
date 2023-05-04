# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AttgroupsItem(scrapy.Item):
    # define the fields for your item here like:

    name = scrapy.Field()
    url = scrapy.Field()
    title_id = scrapy.Field()
    Associated_Groups = scrapy.Field()
    Created = scrapy.Field()
    Last_Modified = scrapy.Field()
    description_body = scrapy.Field()
    Techniques_Used = scrapy.Field()
    Associated_Group_Descriptions = scrapy.Field()
    Software = scrapy.Field()
    stime = scrapy.Field()
