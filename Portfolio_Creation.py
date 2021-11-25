# We import pandas with an alias "pd". Make it easier to work with the pandas functions. Pandas is the best library
# in Python for working with large datasets.
import pandas as pd

# Pyplot is Matplotlib's plotting library. This is used to show some graphs and to test the functions.
from matplotlib import pyplot as plt
import numpy as np

# This is the list of assets that are going to be used. ATM just dummies.
import Styles


def data_preparation():
    df = pd.read_csv("data.csv")
    df = df.iloc[::-1]
    print(df)
    column_list = df.columns[1:]
    for i in column_list:
        df.insert(1, f"{i}_Change", "")
        df[f"{i}_Change"] = df[f"{i}"].pct_change()
        df.insert(1, f"{i}_LogReturn", "")
        df[f"{i}_LogReturn"] = np.log(1 + df[f"{i}_Change"])
        avg_change = df[f"{i}_LogReturn"].mean()
        df.insert(1, f"{i}_Excess", "")

        def excess_calculator(x):
            excess = x - avg_change
            return excess

        df[f"{i}_Excess"] = df[f"{i}_LogReturn"].apply(excess_calculator)

    df_excess = df[["Date", "Cash CHF_Excess", "Bonds CHF_Excess", "Bonds FC (hedged)_Excess", "Swiss Equity_Excess",
                    "Global Equity_Excess", "Global Equity Small Caps_Excess", "EM Equity_Excess", "Real Estate_Excess"]]

    df_raw = df[["Date", "Cash CHF", "Bonds CHF", "Bonds FC (hedged)", "Swiss Equity",
                 "Global Equity", "Global Equity Small Caps", "EM Equity", "Real Estate"]]

    return df_raw, df_excess


# This function creates a portfolio with fixed weights (for now). It is just for testing purposes but it spits out a
# graph with the efficient frontier of all of the given stocks.
def optimal_portfolio():
    df_excess = data_preparation()[1]
    df_raw = data_preparation()[0]

    def covariance_matrix():
        return df_excess.cov()

    cov_matrix = covariance_matrix()

    ind_er = []
    for i in df_raw.columns[1:]:
        ind_er.append((df_raw[i].pct_change().mean())*12)

    ind_er = pd.Series([x for x in ind_er], index=df_raw.columns[1:])

    p_returns = []
    p_volatility = []
    p_weights = []

    num_assets = len(df_raw.columns[1:])
    num_portfolios = 10000

    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights / np.sum(weights)
        p_weights.append(weights)
        returns = np.dot(weights, ind_er)
        p_returns.append(returns)
        var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()  # Portfolio Variance
        sd = np.sqrt(var)
        ann_sd = sd * np.sqrt(12)
        p_volatility.append(ann_sd)

    data = {'Returns': p_returns, 'Volatility': p_volatility}

    for counter, symbol in enumerate(df_raw.columns[1:].tolist()):
        data[symbol + ' weight'] = [w[counter] for w in p_weights]

    # These are all the possible portfolio combinations.
    portfolios = pd.DataFrame(data)
    min_vol_port = portfolios.iloc[portfolios['Volatility'].idxmin()]
    rf = 0.00  # rf is the risk-free interest rate.
    max_sharpe_ratio = portfolios.iloc[((portfolios['Returns'] - rf) / portfolios['Volatility']).idxmax()]

    # The visualization of the efficient frontier.
    # plt.subplots(figsize=[10, 5])
    # plt.scatter(portfolios['Volatility'], portfolios['Returns'], color=Styles.accblue, marker='o', s=10, alpha=0.3)
    # # plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=500)
    # plt.scatter(max_sharpe_ratio[1], max_sharpe_ratio[0], color='r', marker='*', s=500)
    # plt.title("Efficient Portfolio Frontier of Selected Assets")
    # plt.xlabel("Volatility")
    # plt.ylabel("Return")
    # plt.savefig("assets/portfolio.png", dpi=130)
    # plt.show()
    return max_sharpe_ratio[1], max_sharpe_ratio[0]


