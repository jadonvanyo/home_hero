# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# This will define the fields for the HomeItem
class HomeItem(scrapy.Item):
    url = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    beds = scrapy.Field()
    baths = scrapy.Field()
    sqft = scrapy.Field()
    description = scrapy.Field()
    year_built = scrapy.Field()
    property_subtype = scrapy.Field()
    region = scrapy.Field()
    subdivision = scrapy.Field()
    tax_url = scrapy.Field()
    tax = scrapy.Field()
    rent_url = scrapy.Field()
    rent = scrapy.Field()
    min_rent = scrapy.Field()
    max_rent = scrapy.Field()
    structure_quality = scrapy.Field()
    structure_condition = scrapy.Field()