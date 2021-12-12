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
    num_portfolios = 5  # <-- How often is the algorithm supposed to create randomized portfolios to get the most eff.

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
        return asset_selected

    defr = 0.5  # <--  Degrees of Freedom for the Tool.

    # -->   [CA,      BO,   BOFC,   SE,   GE,  GES,  EME,   RE]
    minimum_matrix = {
        '1': [47.50*defr, 0.00*defr, 47.50*defr, 1.00*defr, 0.00*defr, 0.00*defr, 0.00*defr, 4.00*defr],
        '2': [33.78*defr, 16.89*defr, 33.78*defr, 2.07*defr, 1.04*defr, 0.00*defr, 0.00*defr, 10.89*defr],
        '3': [22.17*defr, 25.86*defr, 25.86*defr, 3.48*defr, 3.48*defr, 3.48*defr, 0.00*defr, 15.67*defr],
        '4': [12.67*defr, 25.33*defr, 25.33*defr, 4.58*defr, 4.58*defr, 4.58*defr, 4.58*defr, 18.33*defr],
        '5': [5.28*defr, 23.75*defr, 23.75*defr, 5.90*defr, 5.90*defr, 5.90*defr, 5.90*defr, 23.61*defr],
        '6': [0.00*defr, 21.11*defr, 21.11*defr, 7.22*defr, 7.22*defr, 7.22*defr, 7.22*defr, 28.89*defr],
        '7': [0.00*defr, 15.83*defr, 15.83*defr, 0.00*defr, 13.67*defr, 13.67*defr, 13.67*defr, 27.33*defr],
        '8': [0.00*defr, 21.11*defr, 0.00*defr, 0.00*defr, 0.00*defr, 36.81*defr, 18.41*defr, 23.67*defr],
        '9': [0.00*defr, 10.56*defr, 0.00*defr, 0.00*defr, 0.00*defr, 0.00*defr, 71.57*defr, 17.89*defr],
        '10': [0.00*defr, 0.00*defr, 0.00*defr, 0.00*defr, 0.00*defr, 0.00*defr, 100.0*defr, 0.00*defr],
    }
    risk_cap = 2  # <-- This will be references to the actual risk score the user receives!

    min_weights = list(minimum_matrix[str(risk_cap)])

    # Now, overwrite the min_weights if the asset is not selected at all!
    final_minimums = []
    final_maximums = []
    for item in range(len(constraint_matrix())):
        if constraint_matrix()[item] is True:
            final_minimums.append(min_weights[item])
            final_maximums.append(100.0)
        else:
            final_minimums.append(0.0)
            final_maximums.append(1.0)

    for portfolio in range(num_portfolios):
        weights = np.array(
            [
                np.random.randint(final_minimums[0], final_maximums[0])/100,
                np.random.randint(final_minimums[1], final_maximums[1])/100,
                np.random.randint(final_minimums[2], final_maximums[2])/100,
                np.random.randint(final_minimums[3], final_maximums[3])/100,
                np.random.randint(final_minimums[4], final_maximums[4])/100,
                np.random.randint(final_minimums[5], final_maximums[5])/100,
                np.random.randint(final_minimums[6], final_maximums[6])/100,
                np.random.randint(final_minimums[7], final_maximums[7])/100
            ]
        )

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

    portfolios = pd.DataFrame(data)

    ##################################################################################

    # Save the weights of the given portfolio with max sharpe to sql db.git

    ##################################################################################

    rf = - 0.008  # rf is the risk-free interest rate.
    max_sharpe_ratio = portfolios.iloc[((portfolios['Returns'] - rf) / portfolios['Volatility']).idxmax()]
    print(max_sharpe_ratio)
    print(round(max_sharpe_ratio[1], 4), round(max_sharpe_ratio[0], 4))
    return max_sharpe_ratio[1], max_sharpe_ratio[0]


optimal_portfolio()
