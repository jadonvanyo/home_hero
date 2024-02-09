import scrapy


class TaxspiderSpider(scrapy.Spider):
    name = "taxspider"
    allowed_domains = ["www.countyoffice.org"]
    start_urls = ["https://www.countyoffice.org/"]

    def parse(self, response):
        pass
