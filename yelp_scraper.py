
import datetime
import requests
from bs4 import BeautifulSoup
import os
import csv

#r = requests.get("https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York,+NY&start=1")

csv_headers = ["business_name", "address", "phone"]

def write_products_to_file(filename="listings.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader()
        for product in products:
            writer.writerow(product)

products = []

search_results = range(0,360,30) #may need to hardcode the actual number of search results
for results in search_results:
    r = requests.get(f"https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York,+NY&start={results}")
    #print(r)

    raw = r.text
    soup = BeautifulSoup(raw, "html.parser")

    #soup.find_all("a", {"class":"biz-name"})
    #soup.find_all("div", {"class":"secondary-attributes"})
#
    ##alternatively: soup.select(selector=".biz-name")
#
    #business_name = soup.find_all("a", {"class":"biz-name"})
    #secondary_attributes = soup.find_all("div", {"class":"secondary-attributes"})
#
    #for tag in business_name:
    #    print(tag.text)

    listings = soup.select(selector=".regular-search-result")

    for listing in listings:
        business_name = listing.find("a",{"class":"biz-name"})
        address = listing.find("address")
        phone = listing.find("span",{"class":"biz-phone"})

        d = {"business_name":business_name.text.strip(),"address":address.text.strip(),"phone":phone.text.strip()}

        products.append(d)

        print(d)

        write_products_to_file(products=products)
