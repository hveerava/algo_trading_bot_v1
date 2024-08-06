import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ArbitrageStrategy:
    def __init__(self, stock_data, forex_data, lookback_period=30):
        self.stock_data = stock_data
        self.forex_data = forex_data
        self.lookback_period = lookback_period
        self._validate_params()
        self.df_stock = pd.DataFrame(self.stock_data)
        self.df_forex = pd.DataFrame(self.forex_data)
        self.arbitrage_opportunities = pd.DataFrame()

    def _validate_params(self):
        if not isinstance(self.stock_data, (pd.DataFrame, dict)):
            logging.error("Stock data must be a pandas DataFrame or a dictionary.")
            raise ValueError("Stock data must be a pandas DataFrame or a dictionary.")
        if not isinstance(self.forex_data, (pd.DataFrame, dict)):
            logging.error("Forex data must be a pandas DataFrame or a dictionary.")
            raise ValueError("Forex data must be a pandas DataFrame or a dictionary.")

    def _merge_data(self):
        try:
            self.arbitrage_opportunities = pd.merge(self.df_stock, self.df_forex, on='timestamp')
            logging.info("Data merged successfully.")
        except KeyError:
            logging.error("Timestamp column not found in the data.")
            raise KeyError("Timestamp column not found in the data.")
        except Exception as e:
            logging.error(f"Unexpected error merging data: {str(e)}")
            raise e

    def _calculate_arbitrage_signal(self):
        try:
            self.arbitrage_opportunities['arbitrage_signal'] = (self.arbitrage_opportunities['price_stock'] * self.arbitrage_opportunities['exchange_rate']) - self.arbitrage_opportunities['price_forex']
            self.arbitrage_opportunities['signal'] = self.arbitrage_opportunities['arbitrage_signal'].apply(lambda x: 1 if x > 0 else -1)
            logging.info("Arbitrage signals calculated successfully.")
        except KeyError:
            logging.error("Price columns not found in the data.")
            raise KeyError("Price columns not found in the data.")
        except Exception as e:
            logging.error(f"Unexpected error calculating arbitrage signal: {str(e)}")
            raise e

    def _calculate_returns(self):
        try:
            self.arbitrage_opportunities['returns_stock'] = self.arbitrage_opportunities['price_stock'].pct_change()
            self.arbitrage_opportunities['returns_forex'] = self.arbitrage_opportunities['price_forex'].pct_change()
            self.arbitrage_opportunities['strategy_returns'] = self.arbitrage_opportunities['signal'].shift(1) * (self.arbitrage_opportunities['returns_stock'] - self.arbitrage_opportunities['returns_forex'])
            logging.info("Strategy returns calculated successfully.")
        except Exception as e:
            logging.error(f"Error calculating returns: {str(e)}")
            raise e

    def _drop_na(self):
        try:
            initial_length = len(self.arbitrage_opportunities)
            self.arbitrage_opportunities.dropna(inplace=True)
            final_length = len(self.arbitrage_opportunities)
            logging.info(f"Dropped {initial_length - final_length} rows containing NaN values.")
        except Exception as e:
            logging.error(f"Error dropping NaN values: {str(e)}")
            raise e

    def execute(self):
        try:
            self._merge_data()
            self._calculate_arbitrage_signal()
            self._calculate_returns()
            self._drop_na()
            logging.info("Arbitrage strategy executed successfully.")
            return self.arbitrage_opportunities
        except Exception as e:
            logging.error(f"Error executing Arbitrage Strategy: {str(e)}")
            return pd.DataFrame()

    def plot_performance(self):
        try:
            plt.figure(figsize=(12, 6))
            plt.plot(self.arbitrage_opportunities['timestamp'], self.arbitrage_opportunities['price_stock'], label='Stock Price')
            plt.plot(self.arbitrage_opportunities['timestamp'], self.arbitrage_opportunities['price_forex'], label='Forex Price')
            plt.plot(self.arbitrage_opportunities['timestamp'], self.arbitrage_opportunities['arbitrage_signal'], label='Arbitrage Signal')
            plt.legend()
            plt.title('Arbitrage Strategy Performance')
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
            total_return = self.arbitrage_opportunities['strategy_returns'].sum()
            annualized_return = (1 + total_return) ** (252 / len(self.arbitrage_opportunities)) - 1
            annualized_volatility = self.arbitrage_opportunities['strategy_returns'].std() * np.sqrt(252)
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
