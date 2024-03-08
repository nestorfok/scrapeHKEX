import scrapy
import json
from HKEXscraper2.items import Hkexscraper2Item


class Hkexspider2Spider(scrapy.Spider):
    name = "HKEXspider2"
    allowed_domains = ["www1.hkexnews.hk"]
    start_urls = ["https://www1.hkexnews.hk/index.htm"]

    def start_requests(self):
        url = "https://www1.hkexnews.hk/search/titleSearchServlet.do"

        form_data = {
            'sortDir': '0',
            'sortByOptions': 'DateTime',
            'category': "0",
            'market': "SEHK",
            'stockId': '-1',
            'documentType': "-1",
            'fromDate':"20160101",
            'toDate':"20161231",
            'title': "",
            'searchType': "1",
            't1code': "40000",
            't2Gcode': "-2",
            't2code': "40400",
            'rowRange': "10000",
            'lang': "E"
        }

        yield scrapy.FormRequest(url, method='GET', formdata=form_data, callback=self.parse)
    
    def parse(self, response):
        result = response.json()
        result_list = json.loads(result['result'])

        for item in result_list:
            if '<br/>' in item['STOCK_CODE']:
                stock_codes = item['STOCK_CODE'].split('<br/>')
                print("___________________")
                print(stock_codes)
                for stock_code in stock_codes:
                    row = Hkexscraper2Item()
                    row['stock_code'] = stock_code
                    row['ESG_2017_rel_date'] = 'NA'
                    row['ESG_2018_rel_date'] = 'NA'
                    row['ESG_2019_rel_date'] = 'NA'
                    row['ESG_2020_rel_date'] = 'NA'
                    row['ESG_2021_rel_date'] = 'NA'
                    row['ESG_2022_rel_date'] = 'NA'
                    row['ESG_2023_rel_date'] = 'NA'
                    row['release_date'] = item['DATE_TIME']
                    row['document_name'] = item['TITLE']

                    yield row
            else:
                row = Hkexscraper2Item()
                row['stock_code'] = item['STOCK_CODE']
                row['ESG_2017_rel_date'] = 'NA'
                row['ESG_2018_rel_date'] = 'NA'
                row['ESG_2019_rel_date'] = 'NA'
                row['ESG_2020_rel_date'] = 'NA'
                row['ESG_2021_rel_date'] = 'NA'
                row['ESG_2022_rel_date'] = 'NA'
                row['ESG_2023_rel_date'] = 'NA'
                row['release_date'] = item['DATE_TIME']
                row['document_name'] = item['TITLE']

                yield row