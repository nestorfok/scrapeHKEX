# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HkexscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stock_code = scrapy.Field()
    release_date = scrapy.Field()
    document_name = scrapy.Field()
    # release_date = scrapy.Field()
