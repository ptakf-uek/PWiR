# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyItem(scrapy.Item):
    # define the fields for your item here like:
    address = scrapy.Field()
    port = scrapy.Field()
    country = scrapy.Field()
    pass
