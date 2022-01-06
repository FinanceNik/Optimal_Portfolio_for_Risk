import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt


def monte_carlo_simulation(scenario):
    # --> Scenario can be: ['bull', 'bear', 'neutral']
    if scenario == 'bear':
        expected_returns = 0.03
    elif scenario == 'bull':
        expected_returns = 0.11
    elif scenario == 'neutral':
        expected_returns = 0.05

    investment = 2_000_000
    volatility = 0.14
    duration = 50
    sip = 10000
    final_values = []
    for year in range(duration):
        market_return = np.random.normal(expected_returns, volatility)
        final_value = sip + (1 + market_return) * investment
        investment = final_value
        final_values.append(int(final_value))
    print(final_values)


monte_carlo_simulation('neutral')
