import pandas as pd
import numpy as np
import sqlite3
import Portfolio_Creation as pc


def dataframe_dateRefactoring():
    df = pc.data_preparation()[0]
    df.insert(1, 'Month', '')
    for i in range(len(df.index)):
        month = df['Date'].str.split('/')[i][0]
        df['Month'][i] = month
    return df


def dataframe_construction():
    asset_list = ["CA", "BO", "BOFC", "SE", "GE", "GES", "EME", "RE"]
    df = dataframe_dateRefactoring()
    for asset in asset_list:
        df.insert(2, f"{asset}_weight", "")
    for asset in asset_list:
        df.insert(2, f"{asset}_share", "")
    for asset in asset_list:
        df.insert(2, f"{asset}_value", "")

    df.insert(2, "portfolio_value", "")
    df.insert(3, "period_return", "")

    return df


def dataframe_population_weights():
    df = dataframe_construction()
    for i in range(len(df.index)):
        print(i)
        if df['Month'][i] == '1' or df['Month'][i] == '6':
            print('yes')
        else:
            print('no')

dataframe_population_weights()
