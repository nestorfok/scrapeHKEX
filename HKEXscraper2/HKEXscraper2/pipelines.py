# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class Hkexscraper2Pipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        stock_code = adapter.get('stock_code')
        adapter['stock_code'] = stock_code[1:] + ".HK"

        # Save the release date
        release_date = adapter.get('release_date')
        release_date = release_date.split()[0]
        # adapter['release_date'] = release_date.split()[0]

        # Check which year report the company released
        document_name = adapter.get('document_name')
        document_name = document_name.replace('\n', '')
        year = re.findall(r'\d+', document_name)
        string_year = ','.join(year)

        if "2017" in string_year:
            adapter['ESG_2017_rel_date'] = release_date
        elif '2018' in string_year:
            adapter['ESG_2018_rel_date'] = release_date
        elif '2019' in string_year:
            adapter['ESG_2019_rel_date'] = release_date
        elif '2020' in string_year:
            adapter['ESG_2020_rel_date'] = release_date
        elif '2021' in string_year:
            adapter['ESG_2021_rel_date'] = release_date
        elif '2022' in string_year:
            adapter['ESG_2022_rel_date'] = release_date
        elif '2023' in string_year:
            adapter['ESG_2023_rel_date'] = release_date


        adapter['release_date'] = 'NA'
        adapter['document_name'] = string_year

        # adapter['document_name'] = string_year
        return item
