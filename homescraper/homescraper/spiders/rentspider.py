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
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,lt;q=0.7',
        },
        
        # Give a specific file and format to always save the data to
        'FEEDS': {
            'homedata.json': {'format': 'json', 'overwrite': True}
        },
        
        # Configure custom item pipelines
        'ITEM_PIPELINES': {
        }
    }

    def parse(self, response):
        pass
