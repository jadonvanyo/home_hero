from homescraper.items import HomeItem
import json
import scrapy

class TaxspiderSpider(scrapy.Spider):
    name = "taxspider"
    allowed_domains = ["www.countyoffice.org"]
    start_urls = ["https://www.countyoffice.org/"]
    
        # Overwrite any of the settings.py settings for this particular spider \
    custom_settings = {
        
        # Override the default request headers:
        'DEFAULT_REQUEST_HEADERS': {
            'authority': 'www.countyoffice.org',
            'referer': 'http://www.google.com/',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
        },
        
        # Configure custom item pipelines
        'ITEM_PIPELINES': {
            "homescraper.pipelines.TaxscraperPipeline": 300,
        }
    }

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
            
            # Navigate to the street page with the address numbers
            yield response.follow(tax_url, callback=self.parse_street_page, meta={'address_number': address_number, 'house': house})
        
    def parse_street_page(self, response):
        """Parse the tax page and navigate further based on address_number"""
        
        # Extract address_number and house from meta
        address_number = response.meta.get('address_number')
        house = response.meta.get('house')
         
        # Find the link for the specific house data
        property_page_url = 'https://www.countyoffice.org' + response.xpath(f'//ul/li/a[contains(@href, "{address_number}")]/@href').get()
        
        # Navigate to the property page to pull the required information
        yield response.follow(property_page_url, callback=self.parse_property_page, meta={'house': house})

    def parse_property_page(self, response):
        """Crawl and gather the tax information for a given house"""
        # Extract house data from meta
        house = response.meta.get('house')
        
        # Update the house data with tax information
        house['tax_url'] = response.url
        house['tax'] = response.xpath('//table[contains(@id, "taxes")]/tbody/tr[1]/td[2]/text()').get()
        house['structure_quality'] = response.xpath('//table/tbody/tr/th[contains(text(), "Structure Quality")]/following-sibling::td/text()').get()
        house['structure_condition'] = response.xpath('//table/tbody/tr/th[contains(text(), "Structure Condition")]/following-sibling::td/text()').get()
        
        yield house
        