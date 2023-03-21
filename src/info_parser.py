import requests
from bs4 import BeautifulSoup
import time
import pymongo
from datetime import datetime


class MongoDBHandler:
    def __init__(self, database_url):
        self.client = pymongo.MongoClient(database_url)
        self.db = self.client.get_default_database()
        self.prices = self.db.prices
    
    def store_price(self, karat, price):
        data = {}
        data["karat"] = karat
        data["price"] = float(price.split(" ")[-1])
        data["datetime"] = datetime.utcnow()
        self.prices.insert_one(data).inserted_id
    
    def get_prices(self):
        return self.prices.find({})

# URL of the website to retrieve
url = "https://dubaicityofgold.com/"

db_handler = MongoDBHandler('mongodb://localhost:27020/prices_database')

while True:
    try:
        # Send a GET request to the website and get the HTML content
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract the value you're interested in
        gold_table = soup.find("ul", {"class": "goldtable"}).text.strip()

        # Split the string into lines
        lines = gold_table.split("\n")

        # Loop through each line and extract the data
        for line in lines:
            # Split the line into data components
            data = line.split(" - ")
            karat = data[0]
            price = data[1]
            
            # Print the extracted data
            print("Karat:", karat)
            print("Price:", price)
            db_handler.store_price(karat, price)
        time.sleep(1*60*60)
    except:
        print("error retrieving data!")
        time.sleep(10)
    
    