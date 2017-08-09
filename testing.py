import requests

url = "https://www.etis.ford.com/vehicleSelection.do"

querystring = {"vin":"1FA6P8JZ3H5526063","lookupType":"vin"}

headers = {
    'host': "www.etis.ford.com",
    'connection': "keep-alive",
    'content-length': "36",
    'pragma': "no-cache",
    'cache-control': "no-cache",
    'origin': "https://www.etis.ford.com",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    'content-type': "application/x-www-form-urlencoded",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'dnt': "1",
    'referer': "https://www.etis.ford.com/vehicleRegSelector.do",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-US,en;q=0.8"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
