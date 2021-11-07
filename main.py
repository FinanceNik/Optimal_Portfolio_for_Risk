# We import pandas with an alias "pd". Make it easier to work with the pandas functions. Pandas is the best library
# in Python for working with large datasets.
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import openpyxl

# pandas_datareader is a sub-module of pandas that allows us to call finance APIs to get datasets directly from source.
import pandas_datareader as web

# Datetime is a built-in Python module for working with timed date. In our case we need it to specify the range of the
# Time series.
from datetime import datetime


# This is the function that will be responsible for getting the data and converting it to a pandas dataframe.
# The dataframe allows us to manipulate the data as wanted and is probably the easiest way to work with large datasets
# in Python. Right now I am importing data from the yahoo API engine just to create the algorithms.
# This is just dummy data.
def raw_data_gatherer():
    start = datetime(2015, 1, 1)
    end = datetime(2021, 1, 1)
    tickers = ['AAPL', 'GOOG', 'TSLA']
    dfs = []
    for ticker in tickers:
        stock = web.DataReader(ticker, "yahoo", start, end)
        dfs.append(stock)
    return dfs


# This function takes the raw data gathered by the raw_data_gatherer function and then manipulated it.
# Firstly, the adjusted close columns is renamed to Adjusted to that no spaces are in the name. That could otherwise
# lead to some errors when working with pandas functions down the line.
# Furthermore, we calculate the period return (in this case 1-month return) for each period with the pandas.pct_change
# function. Then we calculate the excess return of each period by getting the average period return overall and
# subtracting that from the one period change. Lastly, the newly adjusted dataframes are returned so we can use them
# for other functions.
def data_prepper():
    assets = raw_data_gatherer()
    dfs = []
    for i in range(len(assets)):
        df_raw = assets[i]
        df = df_raw.rename(columns={"Adj Close": "Adjusted"})
        df.insert(1, 'Change', '')
        df['Change'] = df.Adjusted.pct_change()
        avg_change = df.Change.mean()
        df.insert(1, 'Excess', '')

        def excess_calculator(x):
            excess = x - avg_change
            return excess

        df['Excess'] = df['Change'].apply(excess_calculator)

        dfs.append(df)

    return dfs


