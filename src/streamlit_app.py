import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import matplotlib

matplotlib.use("Agg")


class MongoDBHandler:
    def __init__(self, database_url):
        self.client = MongoClient(database_url)
        self.db = self.client.get_default_database()
        self.prices = self.db.prices
    
    def get_prices(self, start_date=None, end_date=None):
        query = {}
        if start_date and end_date:
            query['datetime'] = {
                '$gte': start_date,
                '$lte': end_date
            }
        else:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            query['datetime'] = {
                '$gte': start_date,
                '$lte': end_date
            }
        return list(self.prices.find(query).sort("datetime", -1))


def time_ago(date):
    now = datetime.now()
    time_diff = now - date
    
    if time_diff.days > 0:
        if time_diff.days == 1:
            return "last day"
        else:
            return f"{time_diff.days} days ago"
    elif time_diff.seconds >= 3600:
        return f"{time_diff.seconds // 3600} hours ago"
    elif time_diff.seconds >= 60:
        return f"{time_diff.seconds // 60} minutes ago"
    else:
        return "less than a minute ago"



if __name__ == "__main__":
    st.set_page_config(page_title="Gold Price")
    st.title("Gold Prices Over Time")
    db_handler = MongoDBHandler("mongodb://localhost:27020/prices_database")

    # Initialize session state
    if "filter_applied" not in st.session_state:
        st.session_state.filter_applied = False
    if "show_home_button" not in st.session_state:
        st.session_state.show_home_button = False

    # Sidebar options
    st.sidebar.header("Filter Options")
    start_date = st.sidebar.date_input("Start Date", datetime(2024, 1, 1))
    end_date = st.sidebar.date_input("End Date", datetime(2024, 12, 31))

    # Apply filter button
    if st.sidebar.button("Apply Filter"):
        st.session_state.filter_applied = True
        st.session_state.show_home_button = True

    # Home button logic
    home_button_placeholder = st.sidebar.empty()
    if st.session_state.show_home_button:
        home_clicked = home_button_placeholder.button("Back")
        if home_clicked:
            st.session_state.filter_applied = False
            st.session_state.show_home_button = False

    # Render content based on state
    if st.session_state.filter_applied:
        # Filtered view
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        prices_data = db_handler.get_prices(start_date=start_datetime, end_date=end_datetime)

        if prices_data:
            data = {
                "Karat": [price["karat"] for price in prices_data],
                "Price": [price["price"] for price in prices_data],
                "Date": [price["datetime"] for price in prices_data]
            }
            df = pd.DataFrame(data)

            st.subheader("Gold Prices Chart")
            fig = px.line(
                df,
                x="Date",
                y="Price",
                color="Karat",
                title="Gold Prices Over Time",
                labels={"Price": "Gold Price", "Date": "Date", "Karat": "Karat"},
            )
            st.plotly_chart(fig, use_container_width=True)

            # get difference in price of 24K gold
            for i in range(4):
                if data["Karat"][i] == "24K":
                    end_price = data["Price"][i]
            
            for i in range(len(data["Karat"])-4, len(data["Karat"])):
                if data["Karat"][i] == "24K":
                    start_price = data["Price"][i]

            st.subheader("Summary")
            st.text(f"Difference: {end_price-start_price:.2f} AED")
            st.text(f"Percentage: {((end_price-start_price)/start_price)*100:.2f} %")

        else:
            st.warning("No data found for the selected date range!")
    else:
        # Home page view
        latest_prices_data = db_handler.get_prices()
        last_price = latest_prices_data[:4]

        if last_price:
            last_data = {}
            for element in last_price:
                if element["karat"] == "18K":
                    last_data["18K"] = [element["price"]]
                elif element["karat"] == "21K":
                    last_data["21K"] = [element["price"]]
                elif element["karat"] == "24K":
                    last_data["24K"] = [element["price"]]
                    date = element["datetime"]
                
            data = {}
            data = {
                "Karat": [price["karat"] for price in latest_prices_data],
                "Price": [price["price"] for price in latest_prices_data],
                "Date": [price["datetime"] for price in latest_prices_data]
            }

            last_df = pd.DataFrame(last_data)
            last_df.reset_index(drop=True)
            df = pd.DataFrame(data)

            st.subheader("Latest Gold Prices Data")
            st.table(last_df)
            st.text(f"Last updated: {time_ago(date)}")

            st.subheader("Latest Gold Prices Chart")
            fig = px.line(
                df,
                x="Date",
                y="Price",
                color="Karat",
                title="Gold Prices Over Time (Last Month)",
                labels={"Price": "Gold Price", "Date": "Date", "Karat": "Karat"},
            )
            st.plotly_chart(fig, use_container_width=True)

            # get difference in price of 24K gold
            for i in range(4):
                if data["Karat"][i] == "24K":
                    end_price = data["Price"][i]
            
            for i in range(len(data["Karat"])-4, len(data["Karat"])):
                if data["Karat"][i] == "24K":
                    start_price = data["Price"][i]

            st.subheader("Summary")
            st.text(f"Difference: {end_price-start_price:.2f} AED")
            st.text(f"Percentage: {((end_price-start_price)/start_price)*100:.2f} %")





        else:
            st.warning("No latest data available.")
