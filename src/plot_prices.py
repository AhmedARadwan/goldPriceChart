import pymongo
import matplotlib.pyplot as plt
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

db_handler = MongoDBHandler('mongodb://localhost:27020/prices_database')

prices = db_handler.get_prices()

data = {}

for price in prices:
    karat = price['karat']
    date = price['datetime']
    value = price['price']
    if karat not in data:
        data[karat] = {'dates': [], 'values': []}
    data[karat]['dates'].append(date)
    data[karat]['values'].append(value)

for karat, karat_data in data.items():
    plt.plot(karat_data['dates'], karat_data['values'], label=f'{karat}K')

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Gold Prices Over Time by Karat')
plt.legend()
plt.show()


















# dates_18K = []
# dates_21K = []
# dates_22K = []
# dates_24K = []
# values_18k = []
# values_21k = []
# values_22k = []
# values_24k = []




# for price in prices:
#     dates.append(price['date'])
#     print(price['karat'])
#     if price['karat'] == "24K":
#         values_24k.append(float(price['price'].split(" ")[-1]))
#     elif price['karat'] == "22K":
#         values_22k.append(float(price['price'].split(" ")[-1]))
#     elif price['karat'] == "21K":
#         values_21k.append(float(price['price'].split(" ")[-1]))
#     elif price['karat'] == "18K":
#         values_18k.append(float(price['price'].split(" ")[-1]))

# plt.plot(dates, values_18k, values_21k, values_22k, values_24k)
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.title('Gold Prices Over Time')
# plt.show()