from homescraper.items import TaxItem
import json
import scrapy

class TaxspiderSpider(scrapy.Spider):
    name = "taxspider"
    allowed_domains = ["www.countyoffice.org"]
    start_urls = ["https://www.countyoffice.org/"]
    # handle_httpstatus_list = [404]  # Handle 404 errors
    
        # Overwrite any of the settings.py settings for this particular spider \
    custom_settings = {
        
        # Override the default request headers:
        'DEFAULT_REQUEST_HEADERS': {
            'authority': 'www.countyoffice.org',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9',
        }, 
        
        # Give a specific file and format to always save the data to
        'FEEDS': {
            'taxdata.json': {'format': 'json', 'overwrite': True}
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
            yield response.follow(tax_url, callback=self.parse_street_page, meta={'address_number': address_number})
        
    def parse_street_page(self, response):
        """Parse the tax page and navigate further based on address_number"""
        
        # Extract address_number from meta
        address_number = response.meta.get('address_number')
        
        # # TODO: Return null for the url and tax if no url is found
        # if response.status == 404:
        #     # Update the JSON with a null value for the target property
        #     update_json_null
        # else:   
        # Find the link for the specific house data
        property_page_url = 'https://www.countyoffice.org' + response.xpath(f'//ul/li/a[contains(@href, "{address_number}")]/@href').get()
        
        # Navigate to the property page to pull the required information
        yield response.follow(property_page_url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        """Crawl and gather the tax information for a given house"""
        
        # TODO: Potentially add structure rating, previous owners, ect from this search
        tax_item = TaxItem()
        tax_item['url'] = response.url
        tax_item['tax'] = response.xpath('//table[contains(@id, "taxes")]/tbody/tr[1]/td[2]/text()').get()
        
        yield tax_item
        
def update_json_null():
    """Update the fields in taxspider.json to null"""
    
    # Set each of the fields to null
    tax_item = TaxItem()
    tax_item['url'] = None
    tax_item['tax'] = None