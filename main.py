import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import openpyxl
import pandas_datareader as web
from datetime import datetime


def raw_data_gatherer():
    start = datetime(2015, 1, 1)
    end = datetime(2021, 1, 1)
    tickers = ['AAPL', 'GOOG', 'TSLA']
    dfs = []
    for ticker in tickers:
        stock = web.DataReader(ticker, "yahoo", start, end)
        dfs.append(stock)
    return dfs


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


