import pandas as pd
import numpy as np
import Data_Handler as dh


def monte_carlo_simulation(scenario):
    df = pd.DataFrame()

    # The number of scenarios that shall be repeated to get the Monte Carlo Simulation
    num_of_scenarios = 1_000

    for i in range(num_of_scenarios):

        # --> Scenario can be: ['bull', 'bear', 'neutral']
        if scenario == 'bear':
            expected_return = 0.03
        elif scenario == 'bull':
            expected_return = 0.11
        elif scenario == 'neutral':
            expected_return = 0.06

        investment = 2_000_000  # <-- Initial Investment set to CHF 2 mil.
        volatility = float(dh.historical_volatility())  # <-- This has to be the volatility of the created portfolio!
        duration = 50  # <-- Duration is set to 50 years to incorporate even very long time-horizons

        lst = []

        for year in range(duration):
            market_return = np.random.normal(expected_return, volatility)
            final_value = (1 + market_return) * investment
            investment = final_value
            lst.append(final_value)
        df[i] = lst

    # print(df)
    mean = int(df.iloc[-1, :].mean())
    std = int(df.iloc[-1, :].std())
    min = int(df.iloc[-1, :].min())
    max = int(df.iloc[-1, :].max())

    return mean, std, min, max
