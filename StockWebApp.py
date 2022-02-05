"""
@Author: Bertan Berker
@Language: Python 3.9.1
@Inspired by: Build A Stock Web Application Using Python
https://www.youtube.com/watch?v=eNDADqa9858

@Data: Pandas API - I am using the Pandas data_reader sub package to
create a dataframe by accessing stock data from Yahoo Finance and
getting stock names from Nasdaq_symbols

This is a stock market dashboard application that shows charts and data regarding certain stocks
"""

# Importing the important libraries for this application
# Stream is being used for building a web app
# Pandas API and data_reader subpackage are used for data manipulation and analysis
# PIL is being used for manipulating, opening and saving various image file types

import streamlit as st
import pandas_datareader.data as pdr
from PIL import Image


# This function basically puts the initial photo for the application
# and creates the sidebar
# :param: No parameters
# :return: Void

def init():
    # Add a title and an image
    st.write("""
      # Stock Market Web Application
      """)
    image = Image.open("C:/Users/berta/Desktop/Personal Projects/Stock Market Web Application/stock_market_image.jpg")

    st.image(image, use_column_width=True)


# This function gets the user input regarding which stock to show
# :param: No parameters
# :return: the start and end dates and the stock symbol for the sidebar

def get_input():
    start_date = st.sidebar.text_input("Start Date", "2017-02-06")
    end_date = st.sidebar.text_input("End Date", "2022-02-03")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "AMZN")
    return start_date, end_date, stock_symbol


# This is the main function that basically calls the necessary functions to load the data
# and initialize the whole program depending on the user input
# :param: No parameters
# :return: Void

def main():
    # Get the user input
    start, end, symbol = get_input()

    try:
        symbol = symbol.upper()

        all_symbols = pdr.get_nasdaq_symbols()
        name = all_symbols.loc[symbol].at["Security Name"]

        if "-" in name:
            name = name.partition("-")[0]
        elif "Common" in name:
            name = name.partition("Common")[0]

        data_frame = pdr.get_data_yahoo(symbol, start=start, end=end)

        init()

        # Display the close price
        st.header(name + "Close Price\n")
        st.line_chart(data_frame["Close"])

        # Display the Volume
        st.header(name + "Volume\n")
        st.line_chart(data_frame["Volume"])

        # Get statistics on the data
        st.header("Data Statistics")
        st.write(data_frame.describe())

    except:
        st.write("""
        # Stock Ticker couldn't be found! TRY AGAIN!!
        """)

        image = Image.open(
            "C:/Users/berta/Desktop/Personal Projects/Stock Market Web Application/error_page.jpg")

        st.image(image, use_column_width=True)


if __name__ == "__main__":
    main()
