import requests

response = requests.get(
  url='https://proxy.scrapeops.io/v1/',
  params={
      'api_key': '4aac2734-0c08-4286-885f-91878b766e16',
      'url': 'https://www.zillow.com/', 
      'residential': 'true', 
      'country': 'us', 
  },
)

print('Response Body: ', response.content)