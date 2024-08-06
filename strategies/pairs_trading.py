import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PairsTradingStrategy:
    def __init__(self, stock_data, benchmark_data, lookback_period=30):
        self.stock_data = stock_data
        self.benchmark_data = benchmark_data
        self.lookback_period = lookback_period
        self._validate_params()
        self.df_stock = pd.DataFrame(self.stock_data)
        self.df_benchmark = pd.DataFrame(self.benchmark_data)
        self.merged_df = pd.DataFrame()

    def _validate_params(self):
        if not isinstance(self.stock_data, (pd.DataFrame, dict)):
            logging.error("Stock data must be a pandas DataFrame or a dictionary.")
            raise ValueError("Stock data must be a pandas DataFrame or a dictionary.")
        if not isinstance(self.benchmark_data, (pd.DataFrame, dict)):
            logging.error("Benchmark data must be a pandas DataFrame or a dictionary.")
            raise ValueError("Benchmark data must be a pandas DataFrame or a dictionary.")
        if not isinstance(self.lookback_period, int) or self.lookback_period <= 0:
            logging.error("Lookback period must be a positive integer.")
            raise ValueError("Lookback period must be a positive integer.")

    def _merge_data(self):
        try:
            self.merged_df = pd.merge(self.df_stock, self.df_benchmark, on='timestamp', suffixes=('_stock', '_benchmark'))
            logging.info("Data merged successfully.")
        except KeyError:
            logging.error("Timestamp column not found in the data.")
            raise KeyError("Timestamp column not found in the data.")
        except Exception as e:
            logging.error(f"Unexpected error merging data: {str(e)}")
            raise e

    def _calculate_spread(self):
        try:
            self.merged_df['spread'] = self.merged_df['price_stock'] - self.merged_df['price_benchmark']
            self.merged_df['mean'] = self.merged_df['spread'].rolling(window=self.lookback_period).mean()
            self.merged_df['std'] = self.merged_df['spread'].rolling(window=self.lookback_period).std()
            self.merged_df['upper_band'] = self.merged_df['mean'] + self.merged_df['std']
            self.merged_df['lower_band'] = self.merged_df['mean'] - self.merged_df['std']
            logging.info("Spread and bands calculated successfully.")
        except KeyError:
            logging.error("Price columns not found in the data.")
            raise KeyError("Price columns not found in the data.")
        except Exception as e:
            logging.error(f"Unexpected error calculating spread: {str(e)}")
            raise e

    def _generate_signals(self):
        try:
            self.merged_df['signal'] = 0
            self.merged_df['signal'][self.merged_df['spread'] < self.merged_df['lower_band']] = 1
            self.merged_df['signal'][self.merged_df['spread'] > self.merged_df['upper_band']] = -1
            logging.info("Trading signals generated successfully.")
        except Exception as e:
            logging.error(f"Error generating trading signals: {str(e)}")
            raise e

    def _calculate_returns(self):
        try:
            self.merged_df['returns_stock'] = self.merged_df['price_stock'].pct_change()
            self.merged_df['returns_benchmark'] = self.merged_df['price_benchmark'].pct_change()
            self.merged_df['strategy_returns'] = self.merged_df['signal'].shift(1) * (self.merged_df['returns_stock'] - self.merged_df['returns_benchmark'])
            logging.info("Strategy returns calculated successfully.")
        except Exception as e:
            logging.error(f"Error calculating returns: {str(e)}")
            raise e

    def _drop_na(self):
        try:
            initial_length = len(self.merged_df)
            self.merged_df.dropna(inplace=True)
            final_length = len(self.merged_df)
            logging.info(f"Dropped {initial_length - final_length} rows containing NaN values.")
        except Exception as e:
            logging.error(f"Error dropping NaN values: {str(e)}")
            raise e

    def execute(self):
        try:
            self._merge_data()
            self._calculate_spread()
            self._generate_signals()
            self._calculate_returns()
            self._drop_na()
            logging.info("Pairs trading strategy executed successfully.")
            return self.merged_df
        except Exception as e:
            logging.error(f"Error executing Pairs Trading Strategy: {str(e)}")
            return pd.DataFrame()

    def plot_performance(self):
        try:
            plt.figure(figsize=(12, 6))
            plt.plot(self.merged_df['timestamp'], self.merged_df['price_stock'], label='Stock Price')
            plt.plot(self.merged_df['timestamp'], self.merged_df['price_benchmark'], label='Benchmark Price')
            plt.plot(self.merged_df['timestamp'], self.merged_df['spread'], label='Spread')
            plt.plot(self.merged_df['timestamp'], self.merged_df['upper_band'], label='Upper Band', linestyle='--')
            plt.plot(self.merged_df['timestamp'], self.merged_df['lower_band'], label='Lower Band', linestyle='--')
            plt.legend()
            plt.title('Pairs Trading Strategy Performance')
            plt.xlabel('Date')
            plt.ylabel('Value')
            plt.grid(True)
            plt.show()
            logging.info("Performance plot generated successfully.")
        except Exception as e:
            logging.error(f"Error plotting performance: {str(e)}")
            raise e

    def calculate_performance_metrics(self):
        try:
            total_return = self.merged_df['strategy_returns'].sum()
            annualized_return = (1 + total_return) ** (252 / len(self.merged_df)) - 1
            annualized_volatility = self.merged_df['strategy_returns'].std() * np.sqrt(252)
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