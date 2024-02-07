import scrapy


class HomespiderSpider(scrapy.Spider):
    name = "homespider"
    allowed_domains = ["www.zillow.com"]
    start_urls = ["https://www.zillow.com/"]

    def parse_zillow_house_page(self, response):
        """Crawl and gather all of the information on a particular house's page"""
        
        # Pull all the data from the table on each page
        table_rows = response.css("table tr")
        # TODO: Create a new HomeItem()
        book_item = BookItem()
        
        book_item['url'] = response.url
        book_item['title'] = response.css('.product_main h1::text').get()
        book_item['upc'] = table_rows[0].css("td ::text").get()
        book_item['product_type'] = table_rows[1].css("td ::text").get()
        book_item['price_excl_tax'] = table_rows[2].css("td ::text").get()
        book_item['price_incl_tax'] = table_rows[3].css("td ::text").get()
        book_item['tax'] = table_rows[4].css("td ::text").get()
        book_item['availability'] = table_rows[5].css("td ::text").get()
        book_item['num_reviews'] = table_rows[6].css("td ::text").get()
        book_item['stars'] = response.css("p.star-rating").attrib['class']
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        book_item['price'] = response.css('p.price_color ::text').get()
            
    def parse(self, response):
        pass
