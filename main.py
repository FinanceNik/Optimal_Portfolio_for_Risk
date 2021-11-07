# We import pandas with an alias "pd". Make it easier to work with the pandas functions. Pandas is the best library
# in Python for working with large datasets.
import pandas as pd

# Pyplot is Matplotlib's plotting library. This is used to show some graphs and to test the functions.
from matplotlib import pyplot as plt
import numpy as np

# pandas_datareader is a sub-module of pandas that allows us to call finance APIs to get datasets directly from source.
import pandas_datareader as web

# Datetime is a built-in Python module for working with timed date. In our case we need it to specify the range of the
# Time series.
from datetime import datetime

# This is the list of assets that are going to be used. ATM just dummies.
assets_used = ['NKE', 'AMZN', 'GOOG']


# This is the function that will be responsible for getting the data and converting it to a pandas dataframe.
# The dataframe allows us to manipulate the data as wanted and is probably the easiest way to work with large datasets
# in Python. Right now I am importing data from the yahoo API engine just to create the algorithms.
# This is just dummy data.
def raw_data_gatherer():
    start = datetime(2015, 1, 1)
    end = datetime(2019, 12, 31)
    tickers = assets_used
    dfs = []
    for ticker in tickers:
        stock = web.DataReader(ticker, "yahoo", start, end)
        dfs.append(stock)
    return dfs


# This function takes the raw data gathered by the raw_data_gatherer function and then manipulated it.
# Firstly, the adjusted close columns is renamed to Adjusted to that no spaces are in the name. That could otherwise
# lead to some errors when working with pandas functions down the line.
# Furthermore, we calculate the period log return (in this case 1-month return) for each period with the
# pandas.pct_change to get the actual change per period. Then we calculate the log return by using the numpy.log
# function. Afterwards, we calculate the excess return of each period by getting the average period log return overall
# and subtracting that from the one period change. Lastly, the newly adjusted dataframes are returned so we can use
# them for other functions.
def data_prepper():
    assets = raw_data_gatherer()
    dfs = []
    for i in range(len(assets)):
        df_raw = assets[i]
        df = df_raw.rename(columns={"Adj Close": "Adjusted"})
        df.insert(1, 'Change', '')
        df['Change'] = df.Adjusted.pct_change()
        df.insert(1, 'LogReturn', '')
        df['LogReturn'] = np.log(1 + df.Change)
        avg_change = df.LogReturn.mean()
        df.insert(1, 'Excess', '')

        def excess_calculator(x):
            excess = x - avg_change
            return excess

        df['Excess'] = df['LogReturn'].apply(excess_calculator)

        dfs.append(df)

    return dfs


# Creation of the Covariance Matrix. This is important for later portfolio optimization.
def covariance_matrix():
    assets = data_prepper()
    names = assets_used
    dfs = []
    for i in range(len(assets)):
        df_raw = assets[i]['Excess']
        df = df_raw.rename(f'{names[i]}')
        dfs.append(df)

    df = pd.concat(dfs, axis=1, ignore_index=False)
    cov_matrix = df.cov()
    return cov_matrix


# This function creates a portfolio with fixed weights (for now). It is just for testing purposes but it spits out a
# graph with the efficient frontier of all of the given stocks.
def optimal_portfolio():
    assets = data_prepper()
    names = assets_used
    dfs = []
    for i in range(len(assets)):
        df_raw = assets[i]['Adjusted']
        df = df_raw.rename(f'{names[i]}')
        dfs.append(df)
    df = pd.concat(dfs, axis=1, ignore_index=False)
    cov_matrix = covariance_matrix()
    ind_er = df.resample('Y').last().pct_change().mean()

    p_returns = []
    p_volatility = []
    p_weights = []

    num_assets = len(df.columns)
    num_portfolios = 10000

    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights / np.sum(weights)
        p_weights.append(weights)
        returns = np.dot(weights, ind_er)
        p_returns.append(returns)
        var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()  # Portfolio Variance
        sd = np.sqrt(var)
        ann_sd = sd * np.sqrt(250)
        p_volatility.append(ann_sd)

    data = {'Returns': p_returns, 'Volatility': p_volatility}

    for counter, symbol in enumerate(df.columns.tolist()):
        data[symbol + ' weight'] = [w[counter] for w in p_weights]

    # These are all the possible portfolio combinations.
    portfolios = pd.DataFrame(data)
    min_vol_port = portfolios.iloc[portfolios['Volatility'].idxmin()]
    rf = 0.00  # rf is the risk-free interest rate.
    max_sharpe_ratio = portfolios.iloc[((portfolios['Returns'] - rf) / portfolios['Volatility']).idxmax()]

    # The visualization of the efficient frontier.
    plt.subplots(figsize=[10, 10])
    plt.scatter(portfolios['Volatility'], portfolios['Returns'], marker='o', s=10, alpha=0.3)
    plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=500)
    plt.scatter(max_sharpe_ratio[1], max_sharpe_ratio[0], color='g', marker='*', s=500)
    plt.show()


optimal_portfolio()







