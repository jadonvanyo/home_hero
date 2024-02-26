import requests

response = requests.get(
  url='https://headers.scrapeops.io/v1/browser-headers',
  params={
      'api_key': '4aac2734-0c08-4286-885f-91878b766e16',
      'num_results': '2'}
)

print(response['sec-ch-ua-platform'])

print('Response Body: ', response.json())