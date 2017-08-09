# import os
import requests

from bs4 import BeautifulSoup


def get_car_details(vin_number):
    '''this should grab the deatils from Fords ETIS site
    and then return something to query the DB with'''

    url = "https://www.etis.ford.com/vehicleSelection.do"

    querystring = {"vin":vin_number,"lookupType":"vin"}
    cookie = {"Ford-eTIS-locale":"language%3Den%2Ccountry%3DUS", "JSESSIONID":"jVYQWM13ZixazSeEQqfUkx_FxKsdPmu1difmIsg6.eccvas1900i"}


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
    print("trying to get the summary of ", vin_number)
    try:
        car_details_html = requests.post(url, headers=headers, data=querystring, cookies=cookie)
    except:
        print("failed")
        return False
    car_details_soup = BeautifulSoup(car_details_html.content, "html.parser")
    # print (car_details_soup)
    something = car_details_soup.find("title")
    print(something)
get_car_details("1FA6P8JZXH5524472")
