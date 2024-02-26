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
        'CLOSESPIDER_ITEMCOUNT': 10,
        
        # Override the default request headers:
        'DEFAULT_REQUEST_HEADERS': {
            'authority': 'www.zillow.com',
            'referer': 'http://www.google.com/',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            # 'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"', 
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"macOS"',
            # 'upgrade-insecure-requests': '1',
            # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            # 'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            # 'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,lt;q=0.7',
        },
        
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
            
    
    # TODO: Create a function to parse through the pages for many houses

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
        
