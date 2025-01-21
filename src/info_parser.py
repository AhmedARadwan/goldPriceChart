import requests
from bs4 import BeautifulSoup
import time
import pymongo
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
        options = Options()
        options.add_argument("--headless")  # Run browser in headless mode
        options.add_argument("--disable-gpu")  # Disable GPU (optional, may improve compatibility)
        options.add_argument("--no-sandbox")  # Bypass OS security model (optional, for Linux)
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.get("https://dubaicityofgold.com")
        time.sleep(5)
        html_content = driver.page_source
        driver.quit()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract the value you're interested in
        gold_prices = {
            '24K': soup.find(id='rate24karat').text.split('-')[-1].strip(),
            '22K': soup.find(id='rate22karat').text.split('-')[-1].strip(),
            '21K': soup.find(id='rate21karat').text.split('-')[-1].strip(),
            '18K': soup.find(id='rate18karat').text.split('-')[-1].strip(),
        }

        # Loop through each item and push data to the database
        for karat, price in gold_prices.items():
            # Print the extracted data
            print("Karat:", karat)
            print("Price:", price)
            db_handler.store_price(karat, price)
        time.sleep(1*60*60)
    except:
        print("error retrieving data!")
        time.sleep(10)
    
    