import pandas as pd
import numpy as np
import sqlite3
import Portfolio_Creation as pc
import Data_Handler as dh

asset_list = ["CA", "BO", "BOFC", "SE", "GE", "GES", "EME", "RE"]


def dataframe_dateRefactoring():
    df = pc.data_preparation()[0]
    df.insert(1, 'Month', '')
    for i in range(len(df.index)):
        month = df['Date'].str.split('/')[i][0]
        df['Month'][i] = month
    return df


def dataframe_construction():
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
    print(df.columns[:])
    data = dh.selected_portfolio_weights()[1]
    data_weights = {"CA": data[0], "BO": data[1], "BOFC": data[2], "SE": data[3],
                    "GE": data[4], "GES": data[5], "EME": data[6], "RE": data[7]}
    for i in range(len(df.index)):
        if df['Month'][i] == '1' or df['Month'][i] == '6':
            for asset in asset_list:
                df[f'{asset}_weight'][i] = data_weights[f"{asset}"]
        else:
            print('')

    df.to_csv('XXX.csv')


dataframe_population_weights()
