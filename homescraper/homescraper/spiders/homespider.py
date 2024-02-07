import scrapy


class HomespiderSpider(scrapy.Spider):
    name = "homespider"
    allowed_domains = ["www.zillow.com"]
    start_urls = ["https://www.zillow.com/"]

    def parse(self, response):
        pass
