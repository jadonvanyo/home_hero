# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class HomescraperPipeline:
    def process_item(self, item, spider):
        """Clean house data before entering it into the json"""
        
        adapter = ItemAdapter(item)
        
        # Convert the address list to a single line
        raw_address = adapter.get('address')
        # Determine that the raw address is a list of more than 1 item
        if len(raw_address) > 1:
            adapter['address'] = raw_address[0] + " " + raw_address[2]
        
        # Remove all the '$' and ',' from price if they are in the price
        if "$" and "," in adapter.get('price'):
            value = adapter.get('price').replace('$', '').replace(',', '')
            adapter['price'] = value
        
        # Test that there is a sqft value
        if not adapter.get('sqft'):
            adapter['sqft'] = "1"
        
        else:
            # Remove all the ' sqft' and ',' from sqft
            value = adapter.get('sqft').replace(' sqft', '').replace(',', '')
            adapter['sqft'] = value
        
        # Remove the multifamily tag, strip, and lowercase for the property subtype
        if ', Multi Family' in adapter.get('property_subtype'):
            value = adapter.get('property_subtype').replace(', Multi Family', '').strip().lower()
            adapter['property_subtype'] = value
        
        return item
    
class TaxscraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        # Remove all the '$' and ',' from tax if they are in the tax
        if "$" and "," in adapter.get('tax'):
            value = adapter.get('tax').replace('$', '').replace(',', '')
            adapter['tax'] = value
        
        return item