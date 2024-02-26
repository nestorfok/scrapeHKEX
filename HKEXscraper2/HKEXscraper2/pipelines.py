# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Hkexscraper2Pipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        stock_code = adapter.get('stock_code')
        adapter['stock_code'] = stock_code[1:] + ".HK"

        release_date = adapter.get('release_date')
        adapter['release_date'] = release_date.split()[0]

        document_name = adapter.get('document_name')
        adapter['document_name'] = document_name.replace('\n', '')

        
        
        return item
