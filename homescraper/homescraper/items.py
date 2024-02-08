# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class HomescraperItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

# This will define the fields for the item
# TODO: Add region, subdivision
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