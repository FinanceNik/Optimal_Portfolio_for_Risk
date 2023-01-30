import pandas as pd
import numpy as np
import sqlite3
import Backtesting
import DataHandler as dh
import Risk_Scoring


def data_preparation():
    # Read the csv file into a Pandas DataFrame in order to work with the data in Python.
    df = pd.read_csv("data.csv")
    # Because the data is sorted from recent to oldest, we reverse the order as working with ascending dates is easier.
    df = df.iloc[::-1]
    # For each column starting from the second one (as python is counting from zero the second column is 1), we want
    # to insert new columns to calculate the percentage change per period for each asset as well as the logarithmic
    # returns from which we calculate the excess returns.
    column_list = df.columns[1:]
    for i in column_list:
        df.insert(1, f"{i}_Change", "")
        df[f"{i}_Change"] = df[f"{i}"].pct_change()
        df.insert(1, f"{i}_LogReturn", "")
        df[f"{i}_LogReturn"] = np.log(1 + df[f"{i}_Change"])
        # Excess return is calculated by subtracting the average change of all periods with the log return of
        # each period.
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

    # Return one dataframe with just the excess returns for each asset for the covariance matrix and the dataframe
    # with no changes to it in order to calculate the asset development from it.
    return df_raw, df_excess


def optimal_portfolio():
    # Retrieve the two datasets from the function above.
    df_excess = data_preparation()[1]
    df_raw = data_preparation()[0]

    # Create the covariance matrix. Most efficiently done by calling the Pandas built-in function .cov() which
    # calculates the covariance of multiple arrays, in this case the whole excess return dataset.
    def covariance_matrix():
        return df_excess.cov(numeric_only=True)

    cov_matrix = covariance_matrix()
    # ind_er as abbreviation to individual asset's expected return
    ind_er = []
    # Starting the columns from the second instance (df[1:]) as in the first instance is just the date.
    for i in df_raw.columns[1:]:
        # Calculating the expected return of each asset by taking the average percentage change of the whole timeframe
        # and then multiplying that by 12 as we have monthly data.
        ind_er.append((df_raw[i].pct_change().mean())*12)
    ind_er = pd.Series([x for x in ind_er], index=df_raw.columns[1:])

    # Initiating empty lists to populate them with the data the function is going to create.
    p_returns = []
    p_volatility = []
    p_weights = []

    # How often is the algorithm supposed to create randomized portfolios to get the one with the highest Sharpe ratio.
    num_portfolios = 10_000

    def constraint_matrix():
        # Retrieve the list of selected and unselected assets from the database.
        def fetch_assets():
            conn = sqlite3.connect('Database.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM asset_constraints")
            rows = cur.fetchmany(size=20)
            assets = [x[1] for x in rows]
            return assets
        # The column names of the asset classes in the dataset.
        all_assets = ['CA', 'BO', 'BOFC', 'SE', 'GE', 'GES', 'EME', 'RE']
        selected_assets = fetch_assets()
        # This is called a list comprehension. This creates a list of true and false values based on whether the
        # asset in the all_assets list is in the selected_assets list. If it is not in there --> False, else True.
        asset_selected = [True if x in selected_assets else False for x in all_assets]
        return asset_selected

    # This was the asset matrix that was more closely tied to the theory. As described in the paper, this matrix did
    # not produce the desired portfolio that were wished for and therefore, we constructed as Asset Inclusion Matrix
    # that includes or excludes asset classes based in its risk/return characteristics depending on the risk scorings
    # of the investor.

    # defr = 0.9  # <--  Degrees of Freedom for the Tool.
    #
    # minimum_matrix = {
    #     '1': [47.50*defr, 0.00*defr, 47.50*defr, 1.00*defr, 0.00*defr, 0.00*defr, 0.00*defr, 4.00*defr],
    #     '2': [33.78*defr, 16.89*defr, 33.78*defr, 2.07*defr, 1.04*defr, 0.00*defr, 0.00*defr, 10.89*defr],
    #     '3': [22.17*defr, 25.86*defr, 25.86*defr, 3.48*defr, 3.48*defr, 3.48*defr, 0.00*defr, 15.67*defr],
    #     '4': [12.67*defr, 25.33*defr, 25.33*defr, 4.58*defr, 4.58*defr, 4.58*defr, 4.58*defr, 18.33*defr],
    #     '5': [5.28*defr, 23.75*defr, 23.75*defr, 5.90*defr, 5.90*defr, 5.90*defr, 5.90*defr, 23.61*defr],
    #     '6': [0.00*defr, 21.11*defr, 21.11*defr, 7.22*defr, 7.22*defr, 7.22*defr, 7.22*defr, 28.89*defr],
    #     '7': [0.00*defr, 15.83*defr, 15.83*defr, 0.00*defr, 13.67*defr, 13.67*defr, 13.67*defr, 27.33*defr],
    #     '8': [0.00*defr, 21.11*defr, 0.00*defr, 0.00*defr, 0.00*defr, 36.81*defr, 18.41*defr, 23.67*defr],
    #     '9': [0.00*defr, 10.56*defr, 0.00*defr, 0.00*defr, 0.00*defr, 0.00*defr, 71.57*defr, 17.89*defr],
    #     '10': [0.00*defr, 0.00*defr, 0.00*defr, 0.00*defr, 0.00*defr, 0.00*defr, 100.0*defr, 0.00*defr],
    # }

    # The Asset inclusion Matrix.

    # Need to have a complementary minimum asset matrix because the asset weights are calculated with a random number
    # generator that needs to have both minimum and maximum values, see lines 177ff.
    # --> (np.random.randint(final_minimums[0], final_maximums[0])/100)

    # Some minor adjustments have been made to the limit cases in order to produce more accurate portfolios.
    # -->   [ CA, BO, BOFC, SE, GE, GES, EME, RE]
    minimum_matrix = {
        '1': [40, 30, 20, 0, 0, 0, 0, 0],
        '2': [35, 25, 15, 0, 0, 0, 0, 0],
        '3': [0, 0, 0, 0, 0, 0, 0, 0],
        '4': [0, 0, 0, 0, 0, 0, 0, 0],
        '5': [0, 0, 0, 0, 0, 0, 0, 0],
        '6': [0, 0, 0, 0, 0, 0, 0, 0],
        '7': [0, 0, 0, 0, 0, 0, 0, 0],
        '8': [0, 0, 0, 0, 0, 0, 0, 0],
        '9': [0, 0, 0, 5, 15, 25, 35, 0],
        '10': [0, 0, 0, 10, 20, 30, 40, 0],
    }

    # Actual Asset Inclusion Matrix as described in the paper. A 100 means asset is included, 1 excluded.

    # -->   [ CA, BO, BOFC, SE, GE, GES, EME, RE]
    maximum_matrix = {
        '1': [100, 100, 100, 1, 1, 1, 1, 1],
        '2': [100, 100, 100, 1, 1, 1, 1, 100],
        '3': [100, 100, 100, 100, 1, 1, 1, 100],
        '4': [100, 100, 100, 100, 100, 1, 1, 100],
        '5': [100, 100, 100, 100, 100, 100, 1, 100],
        '6': [1, 100, 100, 100, 100, 100, 1, 100],
        '7': [1, 100, 100, 100, 100, 100, 100, 100],
        '8': [1, 1, 100, 100, 100, 100, 100, 100],
        '9': [1, 1, 1, 100, 100, 100, 100, 100],
        '10': [1, 1, 1, 100, 100, 100, 100, 1],
    }
    # This try and except clause has been instantiated because the GUI would not run of the user had previously
    # not filled out the questionnaire in full or at all. Then no risk score would be produced and this function would
    # not be able to run. Accordingly, the try and except clause allows the GUI to start regardless of that and then
    # the user can fill out the form properly.
    try:
        # Get the risk scores of the investor and calculate the overall risk score.
        user_risk = Risk_Scoring.risk_willingness_scoring()[1] + Risk_Scoring.risk_capacity_scoring()[1]
        # Match the risk score to the actual matrix.
        min_weights = list(minimum_matrix[str(user_risk)])
        max_weights = list(maximum_matrix[str(user_risk)])

        # Now, overwrite the min_weights if the asset is not selected at all!
        final_minimums = []
        final_maximums = []
        for item in range(len(constraint_matrix())):
            if constraint_matrix()[item] is True:
                final_minimums.append(min_weights[item])
                final_maximums.append(max_weights[item])
            else:
                # Here again, because we create the weights based on a random number generator, we need to have a
                # min and max value. Just chose to be very small together to not throw an error. Actually, the assets
                # won't be in the portfolio anyway if the else clause is triggered.
                final_minimums.append(0.9)
                final_maximums.append(1)

        # This part creates the random asset allocations for the assets that are to be included.
        for portfolio in range(num_portfolios):  # <-- looping over this part 10.000 times.
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
            # Make sure that the sum of all weights together does not go over 100%.
            weights = weights / np.sum(weights)

            p_weights.append(weights)

            # Because Returns are already calculated here, the weight constraints have to be implemented above.
            # The np.dot() function is equivalent to Excels =SUMPRODUCT function.
            returns = np.dot(weights, ind_er)
            p_returns.append(returns)
            # Calculate the variance of the portfolio.
            # the .mul() function is equivalent to Excels =MMULT --> used for matrix multiplication.
            var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()  # Portfolio Variance
            # Calculate the Standard Deviation of the portfolio by taking the square root of the variance.
            sd = np.sqrt(var)
            # Annualize the standard deviation by taking the standard deviation times the square root of 12 for months.
            ann_sd = sd * np.sqrt(12)
            p_volatility.append(ann_sd)

        # Create a tuple with the portfolio returns and volatilities.
        data = {'Returns': p_returns, 'Volatility': p_volatility}

        # The enumerate function is similar to calling a for loop like: for i in range(len(counter)), with performance
        # benefits.
        for counter, symbol in enumerate(df_raw.columns[1:].tolist()):
            data[symbol + ' weight'] = [w[counter] for w in p_weights]

        # Create a DataFrame of all portfolios in order to find the one with the highest Sharpe ratio.
        portfolios = pd.DataFrame(data)

        # The risk-free rate was chosen to still be slightly negative, around -0.8%
        rf = - 0.008  # rf is the risk-free interest rate.
        # Find the portfolio with the highest Sharpe ratio.
        max_sharpe_ratio = portfolios.iloc[((portfolios['Returns'] - rf) / portfolios['Volatility']).idxmax()]

        # Create a list with the indeces, values and the performance characteristics of the portfolio to call
        # functions that write this information to the database so that its fetchable later.
        weight_index = list(max_sharpe_ratio.index)[2:]
        weight_values = list(round(max_sharpe_ratio, 5))[2:]
        portfolio_volatility_AND_return_index = list(max_sharpe_ratio.index)[:2]
        portfolio_volatility_AND_return_values = list(round(max_sharpe_ratio, 5))[:2]

        # Call the functions that write to the database.
        dh.populate_weights(weight_index, weight_values)
        dh.populate_volatility_AND_return(portfolio_volatility_AND_return_index, portfolio_volatility_AND_return_values)
        dh.populate_historical_volatility(max_sharpe_ratio[1])
        Backtesting.backtesting_SQL_population()
        return max_sharpe_ratio[1], max_sharpe_ratio[0]
    except:
        pass


optimal_portfolio()
