import scrapy


class RentspiderSpider(scrapy.Spider):
    name = "rentspider"
    allowed_domains = ["www.zillow.com"]
    start_urls = ["https://www.zillow.com/rental-manager/price-my-rental/"]

    def parse(self, response):
        pass
