
import requests

from bs4 import BeautifulSoup

def get_states():
    states_page = requests.get("http://content.dealerconnection.com/vfs/brands/us_ford_en.html")


def get_cities(state):
    pass

def get_dealer_list(city_url):
    dealer_list_near_city_html = requests.get("http://content.dealerconnection.com/vfs/brands/us/"+city_url)
    dealer_list_near_city = BeautifulSoup(dealer_list_near_city_html.content, "html.parser")
    dealer_listings = dealer_list_near_city.find_all(class_="dealerListing")
    list_to_return = []

    for dealer in dealer_listings:
        details = []
        details.append(dealer.find(class_="dealerName").a.get_text())
        details.append(dealer.find(class_="dealerName").a.get("href"))
        address = dealer.find(class_="dealerAddress").get_text()
        details.append(address.replace("\n", " ").split("Distance")[0].strip())
        phone = dealer.find(class_="dealerPhone").get_text()
        details.append(phone.split('\n')[2])
        list_to_return.append(details)

    return list_to_return
