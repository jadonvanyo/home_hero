import json
import re
import scrapy


class RentspiderSpider(scrapy.Spider):
    name = "rentspider"
    allowed_domains = ["www.zillow.com"]
    start_urls = ["https://www.zillow.com/rental-manager/price-my-rental/"]

        # Overwrite any of the settings.py settings for this particular spider \
    custom_settings = {
        # Override the default request headers:
        'DEFAULT_REQUEST_HEADERS': {
            'authority': 'www.zillow.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
        },
    }

    def parse(self, response):
        """Navigate to the page for each of the houses from homedata.json"""
        
        # Get all of the house data from homedata.json
        with open('homedata.json') as file:
            data = json.load(file)
            
        # Loop through each house in the home data and pull the address information
        for house in data:
            value = house.get('url').split("/")[4].lower()
            rent_url = "https://www.zillow.com/rental-manager/price-my-rental/results/" + value + "/"
        
            # Navigate to the street page with the address numbers
            yield response.follow(rent_url, callback=self.parse_rent_page, meta={'house': house})

    def parse_rent_page(self, response):
        """Crawl and gather the rent information for a given house"""
        # Extract house data from meta
        house = response.meta.get('house')
        
        # Extract javascript script from the page
        javascript = response.xpath('//script[contains(@type, "text/javascript")]/text()').get()
        
        # TODO: Create a smart rent feature to look for the closest rent comp
        # Define the regular expression pattern for the suggested, min, and max comp rents
        suggested_rent_pattern = r'"rentZestimate":(\d+)'
        min_rent_pattern = r'"min":(\d+)'
        max_rent_pattern = r'"max":(\d+)'

        # Search for the pattern in the JavaScript code
        suggested_rent = re.search(suggested_rent_pattern, javascript)
        min_rent = re.search(min_rent_pattern, javascript)
        max_rent = re.search(max_rent_pattern, javascript)
        
        # Update the house data with rent information if it was found
        if suggested_rent and min_rent and max_rent:
            house['rent_url'] = response.url
            house['rent'] = suggested_rent.group(1)
            house['min_rent'] = min_rent.group(1)
            house['max_rent'] = max_rent.group(1)
        
        elif suggested_rent:
            house['rent_url'] = response.url
            house['rent'] = suggested_rent.group(1)
        
        yield house