import pandas as pd
import numpy as np
import Data_Handler as dh


def monte_carlo_simulation(scenario):
    df = pd.DataFrame()

    # The number of scenarios that shall be repeated to get the Monte Carlo Simulation
    num_of_scenarios = 1_000  # <-- Due to long loading times, we could to more iterations.

    for i in range(num_of_scenarios):

        # The expected return is forward-looking and compiled by a sumproduct of the chose portfolio's asset weights
        # times the expected return for each asset under a scenario.
        # --> Scenario can be: ['bull', 'bear', 'neutral']
        if scenario == 'bear':
            expected_return = dh.forward_looking_expected_return('bear')
        elif scenario == 'bull':
            expected_return = dh.forward_looking_expected_return('bull')
        elif scenario == 'neutral':
            expected_return = dh.forward_looking_expected_return('neutral')

        investment = 2_000_000  # <-- Initial Investment set to CHF 2 mil.
        volatility = float(dh.historical_volatility())  # <-- This has to be the volatility of the created portfolio!
        duration = 50  # <-- Duration is set to 50 years to incorporate even very long time-horizons

        lst = []

        # Create a loop that goes over this process 50 times.
        for year in range(duration):
            # np.random.normal creates normally distributed random values based in the two inputs expected return
            # and volatility.
            market_return = np.random.normal(expected_return, volatility)
            # Base the current value on the last value to create a statistical random walk with drift.
            final_value = (1 + market_return) * investment
            investment = final_value
            lst.append(final_value)
        df[i] = lst

    # print(df)
    # --> From the dataframe of all the scenarios, mean, standard deviation, minimum and maximum values are calculated.
    mean = int(df.iloc[-1, :].mean())
    std = int(df.iloc[-1, :].std())
    minimum = int(df.iloc[-1, :].min())
    maximum = int(df.iloc[-1, :].max())
    return mean, std, maximum, minimum
