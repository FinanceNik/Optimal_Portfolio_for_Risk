import pandas as pd
import numpy as np
import sqlite3
import Portfolio_Creation as pc
import Data_Handler as dh
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

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
    markowitz_weights_line = 177
    # loop the whole dataset
    for line in range(177, 0, -6):
        print(line, line-6)

    for i in range(176, 171, -1):
        for asset in asset_list:
            df[f'{asset}_value'][i] = float(df[f'{asset}_share'][177]) * float(df[f'{asset}'][i])

        df['portfolio_value'][i] = float(df['CA_value'][i]) + float(df['BO_value'][i]) + float(df['BOFC_value'][i]) + \
                                   float(df['SE_value'][i]) + float(df['GE_value'][i]) + float(df['GES_value'][i]) + \
                                   float(df['EME_value'][i]) + float(df['RE_value'][i])
        df['portfolio_value'][i] = round(df['portfolio_value'][i], 2)

    # re-balancing part --> always in January and July
    # calculate the portfolio value with asset values based on next period for re-balancing
    portf_rebalancing_value = float(df['CA_share'][177]) * float(df['CA'][171]) + \
                              float(df['BO_share'][177]) * float(df['BO'][171]) + \
                              float(df['BOFC_share'][177]) * float(df['BOFC'][171]) + \
                              float(df['SE_share'][177]) * float(df['SE'][171]) + \
                              float(df['GE_share'][177]) * float(df['GE'][171]) + \
                              float(df['GES_share'][177]) * float(df['GES'][171]) + \
                              float(df['EME_share'][177]) * float(df['EME'][171]) + \
                              float(df['RE_share'][177]) * float(df['RE'][171])
    for asset in asset_list:
        df[f'{asset}_value'][171] = float(df[f'{asset}_weight'][markowitz_weights_line]) * portf_rebalancing_value

    for asset in asset_list:
        df[f'{asset}_share'][171] = float(df[f'{asset}_value'][171]) / float(df[f'{asset}'][171])

    df['portfolio_value'][171] = float(df['CA_value'][171]) + float(df['BO_value'][171]) + float(df['BOFC_value'][171]) + \
                               float(df['SE_value'][171]) + float(df['GE_value'][171]) + float(df['GES_value'][171]) + \
                               float(df['EME_value'][171]) + float(df['RE_value'][171])
    df['portfolio_value'][171] = round(df['portfolio_value'][171], 2)

    df.to_csv('XXX.csv')


dataframe_population_firstYear()

