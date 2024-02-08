import scrapy
from homescraper.items import HomeItem

class HomespiderSpider(scrapy.Spider):
    name = "homespider"
    allowed_domains = ["www.zillow.com"]
    start_urls = ["https://www.zillow.com/homedetails/11801-Franklin-Blvd-Lakewood-OH-44107/33503273_zpid/"]

    def parse_zillow_house_page(self, response):
        """Crawl and gather all of the information on a particular house's page"""
        
        home_item = HomeItem()
        
        home_item['url'] = response.url
        home_item['address'] = response.css('div.styles__AddressWrapper-sc-13x5vko-0.bCvhGr h1::text').getall()
        home_item['price'] = response.css('span[data-testid="price"] span::text').get()
        home_item['beds'] = response.xpath('//ul/li/span[contains(text(), "Bedrooms")]/text()[3]').get()
        home_item['baths'] = response.xpath('//ul/li/span[contains(text(), "Bathrooms")]/text()[3]').get()
        home_item['sqft'] = response.xpath('//ul/li/span[contains(text(), "Total interior livable area")]/text()[3]').get()
        home_item['description'] = response.xpath('//div[contains(@class, "Text-c11n-8-84-3__sc-aiai24-0")]/text()').get()
        home_item['year_built'] = response.xpath('//ul/li/span[contains(text(), "Year built")]/text()[3]').get()
        home_item['property_subtype'] = response.xpath('//ul/li/span[contains(text(), "Property subType")]/text()[3]').get()
        
        yield home_item
        
            
    def parse(self, response):
        pass
