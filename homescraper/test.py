import json


with open('homedata.json') as file:
    data = json.load(file)

for item in data:
    value = item.get('url').split("/")[4].lower()
    value = value.split("-")
    address_number = value[0]
    value = "-".join(value[1:-1])
    new_url = "https://www.countyoffice.org/" + value + "-property-records/"
        ## value = value.split("/")
        ## value = value[4].lower()
        # value = value.split("-", 1)
        # value = value[1][::-1]
        # value = value.split("-", 1)
        # value = value[1][::-1]
    print(address_number)
    print(new_url)

# 1486
# https://www.countyoffice.org/olivewood-ave-lakewood-oh-property-records/
# 2040
# https://www.countyoffice.org/marlowe-ave-lakewood-oh-property-records/
# 11850
# https://www.countyoffice.org/edgewater-dr-apt-212-lakewood-oh-property-records/
# 12929
# https://www.countyoffice.org/plover-st-lakewood-oh-property-records/