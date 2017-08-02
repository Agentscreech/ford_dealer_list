import os
import csv
import math
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty

API = os.environ.get("GOOGLE_API")
geolocator = GoogleV3(API)


#grab all zipcodes from each dealer and check its distance
#if it's less than the radius, then add it to the list to return
def find_in_range(point1):
    for item in os.listdir("./csvs"):
        if item[0] is not ".":
            csv_file = csv.reader(open("./csvs/"+item))
            print("checking ", item)
            #send file to check function
            parse_csv(csv_file)

def parse_csv(csv_file):
    for row in csv_file:
        #send zip to location function
        if len(row[5]) >= 5:
            point2 = get_coords(row[5][0:5])
            distance = math.floor(vincenty(start_coords, point2).miles)
            if distance < int(max_distance):
                results.append(row)
            elif distance > int(max_distance)*1.25:
                #try to keep out of the states that are far way
                #this is totally dependant on the first zipcode listed. Need a better way
                return False


def get_coords(zipcode):
    location = geolocator.geocode(zipcode)
    coords = (location.latitude, location.longitude)
    return coords

if __name__ == "__main__":
    #ask for what zipcode
    start_zip = input("What Zip code are you starting from ")
    start_coords = get_coords(start_zip)

    max_distance = input("How far away do you want to search in miles ")
    results = []
    find_in_range(start_coords)
    #now write the results to a new file
    temp = open("./dealers_in_radius.csv", "w")
    temp.write("Dealer Name,website,street,city,state,zip,phone\n")
    for dealer in results:
        temp.write(dealer[0]+","+dealer[1]+","+dealer[2]+","+dealer[3]+","+dealer[4]+","+dealer[5]+","+dealer[6]+"\n")
    temp.close()
