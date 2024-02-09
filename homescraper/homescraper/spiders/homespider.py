import scrapy
from homescraper.items import HomeItem

class HomespiderSpider(scrapy.Spider):
    name = "homespider"
    allowed_domains = ["www.zillow.com"]
    start_urls = ["https://www.zillow.com/lakewood-oh-44107/duplex/"]

    # Overwrite any of the settings.py settings
    custom_settings = {
        # Close the spider after 2 items have been selected
        'CLOSESPIDER_ITEMCOUNT': 2,
    }

    def parse(self, response):
        """Navigate through each of the houses on a given page"""
        
        # Get all of the links for all the houses on the page
        house_links = response.xpath('//a[contains(@data-test, "property-card-link")]/@href').getall()
        
        # Loop though all of the links to houses on the given zillow page
        for link in house_links:
            # Go into the home page and scrape the data
            yield response.follow(link, callback=self.parse_zillow_house_page)
            

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
        home_item['region'] = response.xpath('//ul/li/span[contains(text(), "Region")]/text()[3]').get()
        home_item['subdivision'] = response.xpath('//ul/li/span[contains(text(), "Subdivision")]/text()[3]').get()
        
        yield home_item
        
