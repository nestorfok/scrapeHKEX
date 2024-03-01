# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Hkexscraper2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stock_code = scrapy.Field()
    ESG_2017_rel_date = scrapy.Field()
    ESG_2018_rel_date = scrapy.Field()
    ESG_2019_rel_date = scrapy.Field()
    ESG_2020_rel_date = scrapy.Field()
    ESG_2021_rel_date = scrapy.Field()
    ESG_2022_rel_date = scrapy.Field()
    ESG_2023_rel_date = scrapy.Field()
    release_date = scrapy.Field()
    document_name = scrapy.Field()
