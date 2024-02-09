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
