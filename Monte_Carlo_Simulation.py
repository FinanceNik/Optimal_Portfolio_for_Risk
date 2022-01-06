import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt

start = dt.datetime(2017, 1, 3)
end = dt.datetime(2017, 12, 31)

prices = web.DataReader('AAPL', 'yahoo', start, end)['Close']
returns = prices.pct_change()

last_price = prices[-1]

# Number of Simulations
num_simulations = 1000
num_days = 252  # <-- Probably have to change this to 12 for months

simulation_df = pd.DataFrame()

for i in range(num_simulations):
    count = 0
    daily_vol = returns.std()

    price_series = []

    price = last_price * (1 + np.random.normal(0, daily_vol))
    price_series.append(price)

    for x in range(num_days):
        if count == 251:  # <-- Have to change this to 12 too for months
            break
        price = price_series[count] * (1 + np.random.normal(0, daily_vol))
        price_series.append(price)
        count += 1

    simulation_df[i] = price_series

fig = plt.figure()
plt.plot(simulation_df)
plt.show()
