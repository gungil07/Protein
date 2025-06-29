import requests

response = requests.get("https://data.rcsb.org/rest/v1/core/entry/1hho")
data = response.json()
print(data)