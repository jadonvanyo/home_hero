import json


with open('homedata.json') as file:
    data = json.load(file)
    value = data[3].get('description')
    print(value)
