import pandas as pd
import numpy as np
import sqlite3


def data_preparation():
    df = pd.read_csv("data.csv")
    df = df.iloc[::-1]
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

    df_excess = df[["Date", "CA_Excess", "BO_Excess", "BOFC_Excess", "SE_Excess",
                    "GE_Excess", "GES_Excess", "EME_Excess",
                    "RE_Excess"]]

    df_raw = df[["Date", "CA", "BO", "BOFC", "SE",
                 "GE", "GES", "EME", "RE"]]

    return df_raw, df_excess


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
    num_portfolios = 5

    def constraint_matrix():

        def fetch_assets():
            conn = sqlite3.connect('Test.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM asset_constraints")
            rows = cur.fetchmany(size=20)
            assets = [x[1] for x in rows]
            return assets
        all_assets = ['CA', 'BO', 'BOFC', 'SE', 'GE', 'GES', 'EME', 'RE']
        selected_assets = fetch_assets()
        asset_selected = [True if x in selected_assets else False for x in all_assets]
        # mins = [0.0 if x is False else 1.0 for x in asset_selected]

    constraint_matrix()
    # -->     CA   BO   BOFC  SE  GE   GES  EME   RE
    minimum_matrix = {
        '1': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '3': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '4': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '5': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '6': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '7': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '8': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '9': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '10': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    }
    risk_cap = 6  # <-- This will be references to the actual risk score the user receives!

    for portfolio in range(num_portfolios):
        a = minimum_matrix[str(risk_cap)]
        weights = np.array([1, 2, 3])
        # print(weights)
        weights = np.random.random(num_assets)
        # print(weights)

        # Create a Matrix with 9 columns and select the weights for each column individually.

        weights = weights / np.sum(weights)

        p_weights.append(weights)

        # Because Returns are already calculated here, the weight constraints have to be implemented above.
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

    ##################################################################################

    # Save the weights of the given portfolio with max sharpe to sql db.git

    ##################################################################################

    rf = - 0.008  # rf is the risk-free interest rate.
    max_sharpe_ratio = portfolios.iloc[((portfolios['Returns'] - rf) / portfolios['Volatility']).idxmax()]

    # #The visualization of the efficient frontier.
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


optimal_portfolio()
