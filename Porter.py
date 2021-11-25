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
import Styles

assets_used = ['^GSPC', 'GC=F', 'GOOG']


def data_prepper():
    start = datetime(2015, 1, 1)
    end = datetime(2019, 12, 31)
    tickers = assets_used
    dfs_raw = []
    for ticker in tickers:
        stock = web.DataReader(ticker, "yahoo", start, end)
        dfs_raw.append(stock)
    assets = dfs_raw
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
    # print(dfs[0])
    return dfs


# This function creates a portfolio with fixed weights (for now). It is just for testing purposes but it spits out a
# graph with the efficient frontier of all of the given stocks.
def optimal_portfolio():
    assets = data_prepper()
    names = assets_used
    dfs = []
    for asset in range(len(assets)):
        df_raw = assets[asset]['Adjusted']
        df = df_raw.rename(f'{names[asset]}')
        dfs.append(df)
    df = pd.concat(dfs, axis=1, ignore_index=False)

    def covariance_matrix():
        dfs_cov = []
        for i in range(len(assets)):
            df_cov_raw = assets[i]['Excess']
            df = df_cov_raw.rename(f'{names[i]}')
            dfs_cov.append(df)
        return pd.concat(dfs_cov, axis=1, ignore_index=False).cov()

    cov_matrix = covariance_matrix()
    ind_er = df.resample('Y').last().pct_change().mean()
    print(ind_er)
    print(type(ind_er))

    p_returns = []
    p_volatility = []
    p_weights = []

    num_assets = len(df.columns)
    num_portfolios = 1000

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
    plt.subplots(figsize=[10, 5])
    plt.scatter(portfolios['Volatility'], portfolios['Returns'], color=Styles.accblue, marker='o', s=10, alpha=0.3)
    # plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=500)
    plt.scatter(max_sharpe_ratio[1], max_sharpe_ratio[0], color='r', marker='*', s=500)
    plt.title("Efficient Portfolio Frontier of Selected Assets")
    plt.xlabel("Volatility")
    plt.ylabel("Return")
    # plt.savefig("assets/portfolio.png", dpi=130)
    # plt.show()


optimal_portfolio()