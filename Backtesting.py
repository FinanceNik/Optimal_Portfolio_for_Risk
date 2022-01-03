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
    for line in range(177, 2, -6):
        try:
            for i in range(line-1, line-6, -1):
                for asset in asset_list:
                    df[f'{asset}_value'][i] = float(df[f'{asset}_share'][line]) * float(df[f'{asset}'][i])

                df['portfolio_value'][i] = float(df['CA_value'][i]) + float(df['BO_value'][i]) + float(df['BOFC_value'][i]) + \
                                           float(df['SE_value'][i]) + float(df['GE_value'][i]) + float(df['GES_value'][i]) + \
                                           float(df['EME_value'][i]) + float(df['RE_value'][i])
                df['portfolio_value'][i] = round(df['portfolio_value'][i], 2)

            # re-balancing part --> always in January and July
            # calculate the portfolio value with asset values based on next period for re-balancing
            portf_rebalancing_value = float(df['CA_share'][line]) * float(df['CA'][line-6]) + \
                                      float(df['BO_share'][line]) * float(df['BO'][line-6]) + \
                                      float(df['BOFC_share'][line]) * float(df['BOFC'][line-6]) + \
                                      float(df['SE_share'][line]) * float(df['SE'][line-6]) + \
                                      float(df['GE_share'][line]) * float(df['GE'][line-6]) + \
                                      float(df['GES_share'][line]) * float(df['GES'][line-6]) + \
                                      float(df['EME_share'][line]) * float(df['EME'][line-6]) + \
                                      float(df['RE_share'][line]) * float(df['RE'][line-6])
            for asset in asset_list:
                df[f'{asset}_value'][line-6] = float(df[f'{asset}_weight'][markowitz_weights_line]) * portf_rebalancing_value

            for asset in asset_list:
                df[f'{asset}_share'][line-6] = float(df[f'{asset}_value'][171]) / float(df[f'{asset}'][171])

            df['portfolio_value'][line-6] = float(df['CA_value'][line-6]) + float(df['BO_value'][line-6]) + float(df['BOFC_value'][line-6]) + \
                                       float(df['SE_value'][line-6]) + float(df['GE_value'][line-6]) + float(df['GES_value'][line-6]) + \
                                       float(df['EME_value'][line-6]) + float(df['RE_value'][line-6])
            df['portfolio_value'][line-6] = round(df['portfolio_value'][line-6], 2)

        # due to the construction of the loop, there will be an error raised on the line nr. 3. This can be excepted
        # as it is not causing any problems.
        except:
            pass

    # now, we are saving the backtesting portfolio values into a database in order to generate a graph later.




