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
        elif len(raw_address) == 1:
            adapter['address'] = raw_address[0]
        
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
        if adapter.get('property_subtype'):
            subtype = self.determine_property_subtype(adapter.get('property_subtype'))
            if subtype is not None:
                adapter['property_subtype'] = subtype
            else:
                if adapter.get('description'):
                    adapter['property_subtype'] = self.determine_property_subtype(adapter.get('description'))
                
        elif adapter.get('description'):
            adapter['property_subtype'] = self.determine_property_subtype(adapter.get('description'))
                    
        return item
    
    
    def determine_property_subtype(self, string):
        """Method to  determine if the property subtype is in a string of text. Return the property subtype if it is and return none otherwise."""
        # Establish a list containing all the property subtypes
        property_subtypes = [
            'duplex',
            'triplex',
            'quadplex',
            'quinplex'
        ]
        
        # Establish a dictionary of other names that might be used to name a property
        additional_property_subtypes = {
            "double": "duplex",
            "2-unit": "duplex",
            "3-unit": "triplex",
            "4-unit": "quadplex"
        }
        
        # Look for each property subtype in the description of the house
        for subtype in property_subtypes:
            if subtype in string.strip().lower():
                return subtype
            
        # Look for additional names for the property subtypes
        for key, value in additional_property_subtypes.items():
            if key in string.strip().lower():
                return value
            
        return None
                    
    
class TaxscraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        # Remove all the '$' and ',' from tax if they are in the tax
        if "$" and "," in adapter.get('tax'):
            value = adapter.get('tax').replace('$', '').replace(',', '')
            adapter['tax'] = value
        
        return item