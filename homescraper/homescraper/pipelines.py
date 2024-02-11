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
        value = adapter.get('address')
        adapter['address'] = value[0] + " " + value[2]
        
        return item
    
class TaxscraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        # Remove all the '$' and ','
        value = adapter.get('tax').replace('$', '').replace(',', '')
        adapter['tax'] = value
        
        return item