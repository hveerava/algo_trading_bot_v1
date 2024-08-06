import pandas as pd
import numpy as np

def simple_moving_average(prices, window=20):
    return prices.rolling(window=window).mean()

def moving_average_crossover(prices, short_window=40, long_window=100):
    signals = pd.DataFrame(index=prices.index)
    signals['short_mavg'] = simple_moving_average(prices, window=short_window)
    signals['long_mavg'] = simple_moving_average(prices, window=long_window)
    signals['signal'] = 0.0
    signals['signal'][short_window:] = np.where(
        signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()
    return signals
