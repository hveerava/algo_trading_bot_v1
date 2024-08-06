import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MeanReversionStrategy:
    def __init__(self, data, lookback_period=20):
        self.data = data
        self.lookback_period = lookback_period
        self._validate_params()
        self.df = pd.DataFrame(self.data)

    def _validate_params(self):
        if not isinstance(self.data, (pd.DataFrame, dict)):
            logging.error("Data must be a pandas DataFrame or a dictionary.")
            raise ValueError("Data must be a pandas DataFrame or a dictionary.")
        if not isinstance(self.lookback_period, int) or self.lookback_period <= 0:
            logging.error("Lookback period must be a positive integer.")
            raise ValueError("Lookback period must be a positive integer.")

    def _calculate_bands(self):
        try:
            self.df['mean'] = self.df['price'].rolling(window=self.lookback_period).mean()
            self.df['std'] = self.df['price'].rolling(window=self.lookback_period).std()
            self.df['upper_band'] = self.df['mean'] + self.df['std']
            self.df['lower_band'] = self.df['mean'] - self.df['std']
            logging.info("Bollinger Bands calculated successfully.")
        except KeyError:
            logging.error("Price column not found in the data.")
            raise KeyError("Price column not found in the data.")
        except Exception as e:
            logging.error(f"Unexpected error calculating Bollinger Bands: {str(e)}")
            raise e

    def _generate_signals(self):
        try:
            self.df['signal'] = 0
            self.df['signal'][self.df['price'] < self.df['lower_band']] = 1
            self.df['signal'][self.df['price'] > self.df['upper_band']] = -1
            logging.info("Trading signals generated successfully.")
        except Exception as e:
            logging.error(f"Error generating trading signals: {str(e)}")
            raise e

    def _calculate_returns(self):
        try:
            self.df['returns'] = self.df['price'].pct_change()
            self.df['strategy_returns'] = self.df['signal'].shift(1) * self.df['returns']
            logging.info("Strategy returns calculated successfully.")
        except Exception as e:
            logging.error(f"Error calculating returns: {str(e)}")
            raise e

    def _drop_na(self):
        try:
            initial_length = len(self.df)
            self.df.dropna(inplace=True)
            final_length = len(self.df)
            logging.info(f"Dropped {initial_length - final_length} rows containing NaN values.")
        except Exception as e:
            logging.error(f"Error dropping NaN values: {str(e)}")
            raise e

    def execute(self):
        try:
            self._calculate_bands()
            self._generate_signals()
            self._calculate_returns()
            self._drop_na()
            logging.info("Mean Reversion strategy executed successfully.")
            return self.df
        except Exception as e:
            logging.error(f"Error executing Mean Reversion Strategy: {str(e)}")
            return pd.DataFrame()

    def plot_performance(self):
        try:
            plt.figure(figsize=(12, 6))
            plt.plot(self.df['timestamp'], self.df['price'], label='Price')
            plt.plot(self.df['timestamp'], self.df['upper_band'], label='Upper Band', linestyle='--')
            plt.plot(self.df['timestamp'], self.df['lower_band'], label='Lower Band', linestyle='--')
            plt.fill_between(self.df['timestamp'], self.df['lower_band'], self.df['upper_band'], color='gray', alpha=0.2)
            plt.legend()
            plt.title('Mean Reversion Strategy Performance')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.grid(True)
            plt.show()
            logging.info("Performance plot generated successfully.")
        except Exception as e:
            logging.error(f"Error plotting performance: {str(e)}")
            raise e

    def calculate_performance_metrics(self):
        try:
            total_return = self.df['strategy_returns'].sum()
            annualized_return = (1 + total_return) ** (252 / len(self.df)) - 1
            annualized_volatility = self.df['strategy_returns'].std() * np.sqrt(252)
            sharpe_ratio = annualized_return / annualized_volatility

            metrics = {
                'Total Return': total_return,
                'Annualized Return': annualized_return,
                'Annualized Volatility': annualized_volatility,
                'Sharpe Ratio': sharpe_ratio
            }

            logging.info(f"Performance metrics calculated: {metrics}")
            return metrics
        except Exception as e:
            logging.error(f"Error calculating performance metrics: {str(e)}")
            raise e