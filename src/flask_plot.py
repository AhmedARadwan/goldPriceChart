import pymongo
from flask import Flask, render_template, jsonify
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime

app = Flask(__name__, template_folder='templates')

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

@app.route('/')
def index():
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
    print("length of 24K values: ", len(data["24K"]['values']))

    fig = make_subplots(rows=len(data), cols=1, subplot_titles=list(data.keys()))

    i = 1
    for karat, karat_data in data.items():
        fig.add_trace(go.Scatter(x=karat_data['dates'], y=karat_data['values'], name=f'{karat}K'), row=i, col=1)
        i += 1

    fig.update_layout(height=800, title_text='Gold Prices Over Time by Karat')
    plot_div = fig.to_html(full_html=True)

    return render_template('index.html', plot_div=plot_div)

@app.route('/update')
def update():
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
    print("length of 24K values: ", len(data["24K"]['values']))

    fig = make_subplots(rows=len(data), cols=1, subplot_titles=list(data.keys()))

    i = 1
    for karat, karat_data in data.items():
        fig.add_trace(go.Scatter(x=karat_data['dates'], y=karat_data['values'], name=f'{karat}K'), row=i, col=1)
        i += 1

    fig.update_layout(height=800, title_text='Gold Prices Over Time by Karat')

    # Convert the Plotly figure to JSON format
    plot_json = fig.to_json()

    # Return the JSON data to the client as a JSON response
    return jsonify(plot_json)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
