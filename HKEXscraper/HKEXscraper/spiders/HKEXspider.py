import scrapy


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
        print("*******************")
        rows = response.css('tbody tr')
        print(rows)
        print("*********")
        for row in rows:
            # td = row.css("td.text-right.text-end.release-time ::text").get()
            stock_code = row.css('td.text-right.text-end.stock-short-code::text').get().strip()
            print(stock_code)
        # print(response.css('td.mobile-list-heading::text').get())
        # print(response.css('tbody tr').get())
        # print(response.xpath("//tr[@role='row']").get())
        # print(t_table)
        print("*******************")
