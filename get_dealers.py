
import requests
import os

from bs4 import BeautifulSoup

def get_states():
    '''returns an dict where abbreviations of states are keys and the states are the value'''
    try:
        states_html = requests.get("http://content.dealerconnection.com/vfs/brands/us_ford_en.html")

    except:
        print("get states page failed")
    states = {}
    states_soup = BeautifulSoup(states_html.content, "html.parser")
    states_list = states_soup.find_all(class_="stateListing")
    for state in states_list:
        link = state.a.get("href")
        abbr = link.split("/")[1].split("_")[0]
        value = state.a.get_text()
        states[abbr] = value

    return states

def get_cities(state):
    '''returns a list of all urls for each city in the state'''
    try:
        city_html = requests.get("http://content.dealerconnection.com/vfs/brands/us/"+state+"_ford_en.html")
    except:
        print("get cities page failed")
    city_urls = []
    cities_soup = BeautifulSoup(city_html.content, "html.parser")
    cities = cities_soup.find_all("li")
    for city in cities:
        city_urls.append(city.a.get("href"))

    return city_urls



def get_dealer_list(city_url):
    '''given a url of a city, returns a list of details: name, url, address, phone'''
    dealer_list_html = requests.get("http://content.dealerconnection.com/vfs/brands/us/"+city_url)
    if dealer_list_html.status_code == 200:
        dealer_list_soup = BeautifulSoup(dealer_list_html.content, "html.parser")
        dealer_listings = dealer_list_soup.find_all(class_="dealerListing")
        list_of_details = []

        for dealer in dealer_listings:
            details = []
            details.append(dealer.find(class_="dealerName").a.get_text()) # dealer name
            details.append(dealer.find(class_="dealerName").a.get("href")) # dealer web address
            address = dealer.find(class_="dealerAddress").get_text().split("\n\n")
            details.append(address[0].strip()) # street
            details.append(address[1].split('\n')[0]) # city
            details.append(address[1].split('\n')[2].strip()) #state
            details.append(address[1].split('\n')[3].split('-')[0].strip()) #zipcode
            phone = dealer.find(class_="dealerPhone").get_text()
            details.append(phone.split('\n')[2]) #dealer phone sanitized
            list_of_details.append(details)
    if list_of_details:
        return list_of_details

def add_to_csv(array_to_add, state_csv):
    '''takes the array_to_add and adds each index's properties to a file for each state'''
    print("adding details to ", state_csv)
    writing_file = open(state_csv, "a")
    for dealer_details in array_to_add:
        for index, detail_str in enumerate(dealer_details):
            if "," in detail_str:
                print("trying to replace commas in ", detail_str)
                dealer_details[index] = detail_str.replace(',', ' ')
                # print("after replacement ")
        writing_file.write(dealer_details[0]+","+dealer_details[1]+","+dealer_details[2]+","+dealer_details[3]+","+dealer_details[4]+","+dealer_details[5]+","+dealer_details[6]+"\n")
    writing_file.close()
        #add each item to the csv

if __name__ == "__main__":

    state_listings = get_states()
    #create a new .csv for each state
    for state_abbr in state_listings:
        print(state_abbr, " ", end="")
        temp = open("./csvs/"+state_listings[state_abbr]+".csv", "w")
        temp.write("Dealer Name,website,street,city,state,zip,phone\n")
        temp.close()
    master_list = []
    state_selected = input("input a state abbreviation please: ")
    if state_selected.lower() in state_listings:
        found_cities = get_cities(state_selected.lower())
        for url_for_city in found_cities:
            detail_list = get_dealer_list(url_for_city)
            for detail in detail_list:
                if detail not in master_list:
                    master_list.append(detail)
        add_to_csv(master_list, "./csvs/"+state_listings[state_selected.lower()]+".csv")
    else:
        print("sorry that wasn't a valid input.  Exiting")
