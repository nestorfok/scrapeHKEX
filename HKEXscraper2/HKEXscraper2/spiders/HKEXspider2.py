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
            'fromDate':"20230122",
            'toDate':"20230826",
            'title': "",
            'searchType': "1",
            't1code': "40000",
            't2Gcode': "-2",
            't2code': "40400",
            'rowRange': "50",
            'lang': "E"
        }

        yield scrapy.FormRequest(url, method='GET', formdata=form_data, callback=self.parse)
    
    def parse(self, response):
        result = response.json()
        result_list = json.loads(result['result'])

        for item in result_list:
            row = Hkexscraper2Item()
            row['stock_code'] = item['STOCK_CODE']
            row['release_date'] = item['DATE_TIME']
            row['document_name'] = item['TITLE']

            yield row