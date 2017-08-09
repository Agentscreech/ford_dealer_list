# import os
import requests

from bs4 import BeautifulSoup


def get_car_details(vin_number):
    '''this should grab the deatils from Fords ETIS site
    and then return something to query the DB with'''

    url = "https://www.etis.ford.com/vehicleSelection.do"
    set_cookies = requests.get(url)
    querystring = {"vin":vin_number,"lookupType":"vin"}

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
        car_details_html = requests.post(url, headers=headers, data=querystring, cookies=set_cookies.cookies)
    except:
        print("failed")
        return False
    car_details_soup = BeautifulSoup(car_details_html.content, "html.parser")
    print(car_details_soup.find("title").get_text()) # shoule be Vehical Summary
    primary_features_section = car_details_soup.find(id="pfcSummary")
    primary_features = primary_features_section.find_all(class_="summaryContent")
    options = {}
    options["Build Date"] = primary_features[0].get_text().split("\xa0\xa0")[1]
    options["Color"] = primary_features[-1].get_text()

    #now to the minor feature list
    #Vehicle Cover B == painted black roof
    #Accent Stripe-<data I want> = Stripe
    #SVT-R Package = R model
    #With Temp Control Driver Seat = convenience Package
    #With Navigation System && Less Temp Control Driver Seat = Electronics Package
    minor_features_section = car_details_soup.find(id="mfcList")
    minor_features = minor_features_section.find_all("li")
    for feature in minor_features:
        feature = feature.get_text()
        if "Vehicle Cover B" in feature:
            options["Painted Black Roof"] = True
        if "Accent Stripe-" in feature:
            options["Over the Top Racing Stripe"] = feature.split("-")[1]
        if "With Temp Control Driver Seat" in feature:
            options["Convenience Package"] = True
        if "With Navigation" in feature:
            options["has nav"] = True
        if "SVT-R Package" in feature:
            options["R Model"] = True

    #check for electronic or convienence Package
    if "has nav" in options and "Convenience Package" not in options:
        options.pop("has nav", None)
        options["Electronics Pacakge"] = True
    elif "Convenience Pacakge" in options:
        options.pop("has nav", None)

    return options
