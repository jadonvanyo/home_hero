from homescraper.items import TaxItem
import json
import scrapy

# TODO: Change the DEFAULT_REQUEST_HEADERS in settings

##################### WARNING #########################
# DO NOT RUN THIS SPIDER, IT IS NOT READY FOR USE

class TaxspiderSpider(scrapy.Spider):
    name = "taxspider"
    allowed_domains = ["www.countyoffice.org"]
    start_urls = ["https://www.countyoffice.org/"]

    def parse(self, response):
        """Navigate to the page for each of the houses from homedata.json"""
        
        # Get all of the house data from homedata.json
        with open('homedata.json') as file:
            data = json.load(file)
            
        # Loop through each house in the home data and pull the address information
        for house in data:
            value = house.get('url').split("/")[4].lower()
            value = value.split("-")
            address_number = value[0]
            value = "-".join(value[1:-1])
            tax_url = "https://www.countyoffice.org/" + value + "-property-records/"
            
            # TODO: Navigate to one page, then navigate to the property details page
            yield response.follow(tax_url, callback=self.parse_county_office_page)
        

    def parse_county_office_page(self, response):
        """Crawl and gather the tax information for a give house"""
        
        home_item = TaxItem()
        home_item['url'] = response.url
        # TODO: Correct the response for this item
        home_item['tax'] = response.css('div.styles__AddressWrapper-sc-13x5vko-0.bCvhGr h1::text').getall()
        
        yield home_item