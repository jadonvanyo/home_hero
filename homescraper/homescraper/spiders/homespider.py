import scrapy
from homescraper.items import HomeItem
from analysis_functions import load_json

class HomespiderSpider(scrapy.Spider):
    name = "homespider"
    allowed_domains = ["www.zillow.com"]
    
    # Load config file with all the start urls
    start_urls = load_json("config.json")['starturls']

    # Overwrite any of the settings.py settings for this particular spider \
    custom_settings = {
        # Close the spider after a certain number of items have been scraped
        # 'CLOSESPIDER_ITEMCOUNT': 10,
        
        # Override the default request headers:
        'DEFAULT_REQUEST_HEADERS': {
            'authority': 'www.zillow.com',
            'referer': 'http://www.google.com/',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
        },
         # TODO: DELETE this
        # Give a specific file and format to always save the data to
        'FEEDS': {
            'homedata.json': {'format': 'json', 'overwrite': True}
        },
        
        # Configure custom item pipelines
        'ITEM_PIPELINES': {
            "homescraper.pipelines.HomescraperPipeline": 300,
        }
    }

    def parse(self, response):
        """Navigate through each of the houses on a given page"""
        
        # Get all of the links for all the houses on the page
        house_links = response.xpath('//div[1]/ul/li/div/div/article/div/div/a[contains(@data-test, "property-card-link")]/@href').getall()
        
        # Loop though all of the links to houses on the given zillow page
        for link in house_links:
            # Go into the home page and scrape the data
            yield response.follow(link, callback=self.parse_zillow_house_page)
            
        # Load in the next page
        next_page = response.xpath('//a[contains(@title, "Next page")][contains(@aria-disabled, "false")]/@href').get()
        
        # Determine if there is still a next page
        if next_page is not None:
            # TODO: verify that this is correct
            next_page_url = "https://www.zillow.com" + next_page
            # Follow the next page and perform the callback function on the response from following the page
            yield response.follow(next_page_url, callback=self.parse)
            

    def parse_zillow_house_page(self, response):
        """Crawl and gather all of the information on a particular house's page"""
        
        home_item = HomeItem()
        home_item['url'] = response.url
        home_item['address'] = response.xpath('//div[contains(@data-testid, "fs-chip-container")]/div/div/div/h1/text()').getall()
        home_item['price'] = response.css('span[data-testid="price"] span::text').get()
        home_item['beds'] = response.xpath('//ul/li/span[contains(text(), "Bedrooms")]/text()[3]').get()
        home_item['baths'] = response.xpath('//ul/li/span[contains(text(), "Bathrooms")]/text()[3]').get()
        home_item['sqft'] = response.xpath('//ul/li/span[contains(text(), "Total interior livable area")]/text()[3]').get()
        home_item['description'] = response.xpath('//article/div/div/text()').get()
        home_item['year_built'] = response.xpath('//ul/li/span[contains(text(), "Year built")]/text()[3]').get()
        home_item['property_subtype'] = response.xpath('//ul/li/span[contains(text(), "Property subType")]/text()[3]').get()
        home_item['region'] = response.xpath('//ul/li/span[contains(text(), "Region")]/text()[3]').get()
        home_item['subdivision'] = response.xpath('//ul/li/span[contains(text(), "Subdivision")]/text()[3]').get()
        
        yield home_item
        
