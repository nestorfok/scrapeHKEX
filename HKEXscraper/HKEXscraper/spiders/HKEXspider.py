import scrapy
from HKEXscraper.items import HkexscraperItem


class HkexspiderSpider(scrapy.Spider):
    name = "HKEXspider"
    allowed_domains = ["hkexnews.hk", "www1.hkexnews.hk"]
    start_urls = ["https://www.hkexnews.hk/index.htm"]

    def start_requests(self):
        form_data = {
            'lang': "EN",
            'category': "0",
            'market': "SEHK",
            'searchType': "1",
            'documentType': "-1",
            't1code': "40000",
            't2Gcode': "-2",
            't2code': "40400",
            'from': "20240122",
            'to': "20240222",
        }

        yield scrapy.FormRequest(url = "https://www1.hkexnews.hk/search/titlesearch.xhtml", formdata = form_data, callback = self.parse)

    def parse(self, response):
        # print("*******************")
        rows = response.css('tbody tr')
        # print(rows)
        # print("*********")
        for row in rows:
            # td = row.css("td.text-right.text-end.release-time ::text").get()
            item = HkexscraperItem()

            item['stock_code'] = row.css('td.text-right.text-end.stock-short-code::text').get()
            item['release_date'] = row.css('td.release-time::text').getall()[1]
            item['document_name'] = row.css('td div.headline::text').get()

            yield item
            # stock_code = row.css('td.text-right.text-end.stock-short-code::text').get()
            # print(stock_code)
            # release_date = row.css('td.release-time::text').getall()[1]
            # print(release_date)
            # document_name = row.css('td div.headline::text').get()
            # print(document_name)
        # print(response.css('td.mobile-list-heading::text').get())
        # print(response.css('tbody tr').get())
        # print(response.xpath("//tr[@role='row']").get())
        # print(t_table)
        # print("*******************")
