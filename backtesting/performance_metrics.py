import numpy as np

class PerformanceMetrics:
    def __init__(self, returns):
        self.returns = returns

    def calculate_metrics(self):
        try:
            total_return = self.returns.sum()
            annualized_return = (1 + total_return) ** (252 / len(self.returns)) - 1
            annualized_volatility = self.returns.std() * np.sqrt(252)
            sharpe_ratio = annualized_return / annualized_volatility

            print(f"Total Return: {total_return:.2f}")
            print(f"Annualized Return: {annualized_return:.2f}")
            print(f"Annualized Volatility: {annualized_volatility:.2f}")
            print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
        except Exception as e:
            print(f"Error calculating performance metrics: {str(e)}")
