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
    data = dh.selected_portfolio_weights()[1]
    data_weights = {"CA": data[0], "BO": data[1], "BOFC": data[2], "SE": data[3],
                    "GE": data[4], "GES": data[5], "EME": data[6], "RE": data[7]}
    for i in range(len(df.index)):
        if df['Month'][i] == '1' or df['Month'][i] == '7':
            for asset in asset_list:
                df[f'{asset}_weight'][i] = data_weights[f"{asset}"]
        else:
            pass
    return df


def dataframe_population_firstRow():
    df = dataframe_population_weights()
    df['portfolio_value'][177] = 100_000
    df['period_return'][177] = 0.0
    for asset in asset_list:
        df[f'{asset}_value'][177] = df[f'{asset}_weight'][177] * df['portfolio_value'][177]

    for asset in asset_list:
        df[f'{asset}_share'][177] = float(df[f'{asset}_value'][177]) / float(df[f'{asset}'][177])

    return df


def dataframe_population_firstYear():
    df = dataframe_population_firstRow()
    for i in range(176, 171, -1):
        for asset in asset_list:
            try:
                df[f'{asset}_value'][i] = float(df[f'{asset}_share'][177]) * float(df[f'{asset}'][i])
            except:
                df[f'{asset}_value'][i] = 0.0
        df['portfolio_value'][i] = float(df['CA_value'][i]) + float(df['BO_value'][i]) + float(df['BOFC_value'][i]) + \
                                   float(df['SE_value'][i]) + float(df['GE_value'][i]) + float(df['GES_value'][i]) + \
                                   float(df['EME_value'][i]) + float(df['RE_value'][i])
        df['portfolio_value'][i] = round(df['portfolio_value'][i], 2)

    for asset in asset_list:
        try:
            df[f'{asset}_value'][171] = float(df[f'{asset}_weight'][171]) * float(df['portfolio_value'][171+1])
        except:
            df[f'{asset}_value'][171] = 0.0

    for asset in asset_list:
        df[f'{asset}_share'][171] = float(df[f'{asset}_value'][171]) / float(df[f'{asset}'][171])

    df['portfolio_value'][171] = float(df['CA_value'][171]) + float(df['BO_value'][171]) + float(df['BOFC_value'][171]) + \
                               float(df['SE_value'][171]) + float(df['GE_value'][171]) + float(df['GES_value'][171]) + \
                               float(df['EME_value'][171]) + float(df['RE_value'][171])
    df['portfolio_value'][171] = round(df['portfolio_value'][171], 2)

    df.to_csv('XXX.csv')


dataframe_population_firstYear()

