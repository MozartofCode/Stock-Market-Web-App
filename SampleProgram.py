"""
@Author: Bertan Berker
@Language: Python 3.9.1
@Inspired by: Build A Stock Web Application Using Python
https://www.youtube.com/watch?v=eNDADqa9858
@Data: Downloaded the data files (.csv) from Yahoo Finance's Website
This is a stock market dashboard application that shows charts and data regarding certain stocks
"""

# Importing the important libraries for this application
# Stream is being used for building a web app
# Pandas is used for data manipulation and analysis
# PIL is being used for manipulating, opening and saving various image file types

import streamlit as st
import pandas as pd
from PIL import Image


# This function basically puts the initial photo for the application
# and creates the sidebar
# :param: No parameters
# :return: Void

def init():
    # Add a title and an image
    st.write("""
    # Stock Market Web Application
    **Visually** show data on a stock! Date range from February 6, 2017 - February 3, 2022
    """)

    image = Image.open("C:/Users/berta/Desktop/Personal Projects/Stock Market Web Application/stock_market_image.jpg")

    st.image(image, use_column_width=True)

    # Create a sidebar header
    st.sidebar.header("User Input")


# This function gets the user input regarding which stock to show
# :param: No parameters
# :return: the start and end dates and the stock symbol for the sidebar

def get_input():
    start_date = st.sidebar.text_input("Start Date", "2017-02-06")
    end_date = st.sidebar.text_input("End Date", "2022-02-03")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "AMZN")
    return start_date, end_date, stock_symbol


# This function gets the company's name from the given input
# :param symbol: This is the symbol (ticker) of the stock the user is searching
# :return: The name of the company based on the Ticker (empty string if company not in database)

def get_company_name(symbol):
    if symbol == "AMZN":
        return "Amazon"
    elif symbol == "TSLA":
        return "Tesla"
    elif symbol == "GOOG":
        return "Alphabet"
    else:
        return None


# This function gets the proper company data and the proper timeframe from the users inputs
# :param symbol: Stock ticker
# :param start: The start date for the stock
# :param end: The end date for the stock
# :return: Data information from the chosen database

def get_data(symbol, start, end):
    # Load the file
    if symbol.upper() == "AMZN":
        data_frame = pd.read_csv(
            r"C:\Users/berta/Desktop/Personal Projects/Stock Market Web Application/AMZN.csv")
    elif symbol.upper() == "TSLA":
        data_frame = pd.read_csv(
            r"C:\Users/berta/Desktop/Personal Projects/Stock Market Web Application/TSLA.csv")
    elif symbol.upper() == "GOOG":
        data_frame = pd.read_csv(
            r"C:\Users/berta/Desktop/Personal Projects/Stock Market Web Application/GOOG.csv")
    else:
        data_frame = pd.DataFrame(
            columns=["Data", "Close", "Open", "Volume", "Adj Close", "High", "Low"])

    # Get the Data range
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    # Set the start and end index rows both to 0
    start_row = 0
    end_row = 0

    for i in range(0, len(data_frame)):
        if start <= pd.to_datetime(data_frame["Date"][i]):
            start_row = i
            break

    for j in range(0, len(data_frame)):
        if end >= pd.to_datetime(data_frame["Date"][len(data_frame) - 1 - j]):
            end_row = len(data_frame) - 1 - j
            break

    # Set the index to be the date
    data_frame = data_frame.set_index(pd.DatetimeIndex(data_frame["Date"].values))

    return data_frame.iloc[start_row:end_row + 1, :]


# This is the main function that basically calls the necessary functions to load the data
# and initialize the whole program depending on the user input
# :param: No parameters
# :return: Void

def main():

    init()

    # Get the user input
    start, end, symbol = get_input()


    # Get the company name
    company_name = get_company_name(symbol.upper())

    try:
        # Get the data
        data_frame = get_data(symbol, start, end)

        # Display the close price
        st.header(company_name + " Close Price\n")
        st.line_chart(data_frame["Close"])

        # Display the Volume
        st.header(company_name + " Volume\n")
        st.line_chart(data_frame["Volume"])

        # Get statistics on the data
        st.header("Data Statistics")
        st.write(data_frame.describe())

    except:
        st.header("INVALID TICKER\n")


if __name__ == "__main__":
    main()
