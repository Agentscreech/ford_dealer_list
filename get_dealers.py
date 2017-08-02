
import requests

from bs4 import BeautifulSoup

def get_states():
    '''returns an dict where abbreviations of states are keys and the states are the value'''
    try:
        states_html = requests.get("http://content.dealerconnection.com/vfs/brands/us_ford_en.html")

    except:
        print("get states page failed")
    states = {}
    states_page = BeautifulSoup(states_html, "html.parser")
    states_soup = states_page.find_all(class_="stateListing")
    for state in states_soup:
        link = state.a.get("href")
        abbr = link.split("/")[1].split("_")[0]
        value = state.a.get_text()
        states[abbr] = value

    return states

def get_cities(state):
    pass

def get_dealer_list(city_url):
    '''given a url of a city, returns a list of details: name, url, address, phone'''
    dealer_list_html = requests.get("http://content.dealerconnection.com/vfs/brands/us/"+city_url)
    if dealer_list_html.status_code == 200:
        dealer_list_soup = BeautifulSoup(dealer_list_html.content, "html.parser")
        dealer_listings = dealer_list_soup.find_all(class_="dealerListing")
        list_to_return = []

        for dealer in dealer_listings:
            details = []
            details.append(dealer.find(class_="dealerName").a.get_text()) # dealer name
            details.append(dealer.find(class_="dealerName").a.get("href")) # dealer web address
            address = dealer.find(class_="dealerAddress").get_text()
            details.append(address.replace("\n", " ").split("Distance")[0].strip()) #dealer address sanitized
            phone = dealer.find(class_="dealerPhone").get_text()
            details.append(phone.split('\n')[2]) #dealer phone sanitized
            list_to_return.append(details)
    if len(list_to_return) > 0:
        return list_to_return

def add_to_csv(array_to_add):
    '''takes the array_to_add and adds each index's properties to a file'''
    for dealer_details in array_to_add:

        for detail in dealer_details:

            #add each item to the csv
