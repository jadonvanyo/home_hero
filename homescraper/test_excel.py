address_list = [
  "https://proxy.scrapeops.io/v1/?api_key=d875dca3-61b5-4126-9181-24e588fe58d3&url=https%3A%2F%2Fwww.zillow.com%2Fhomedetails%2F1486-Olivewood-Ave-Lakewood-OH-44107%2F33499525_zpid%2F",
  "https://proxy.scrapeops.io/v1/?api_key=d875dca3-61b5-4126-9181-24e588fe58d3&url=https%3A%2F%2Fwww.zillow.com%2Fhomedetails%2F12929-Plover-St-Lakewood-OH-44107%2F33504136_zpid%2F", 
  "https://proxy.scrapeops.io/v1/?api_key=d875dca3-61b5-4126-9181-24e588fe58d3&url=https%3A%2F%2Fwww.zillow.com%2Fhomedetails%2F2040-Marlowe-Ave-Lakewood-OH-44107%2F33500906_zpid%2F",
  "https://proxy.scrapeops.io/v1/?api_key=d875dca3-61b5-4126-9181-24e588fe58d3&url=https%3A%2F%2Fwww.zillow.com%2Fhomedetails%2F2200-Lewis-Dr-Lakewood-OH-44107%2F33503639_zpid%2F",
  "https://proxy.scrapeops.io/v1/?api_key=d875dca3-61b5-4126-9181-24e588fe58d3&url=https%3A%2F%2Fwww.zillow.com%2Fhomedetails%2F1233-Granger-Ave-Lakewood-OH-44107%2F33489850_zpid%2F",
  "https://proxy.scrapeops.io/v1/?api_key=d875dca3-61b5-4126-9181-24e588fe58d3&url=https%3A%2F%2Fwww.zillow.com%2Fhomedetails%2F11801-Franklin-Blvd-Lakewood-OH-44107%2F33503273_zpid%2F"
]


for address in address_list:
  value = address.split("%2F")[4].lower()
  print(value)
  