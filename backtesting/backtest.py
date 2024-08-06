import pandas as pd
from .performance_metrics import PerformanceMetrics
import logging

def backtest_strategy(signals):
    try:
        df = pd.DataFrame(signals)
        df['strategy_returns'] = df['price'].pct_change() * df['signal'].shift(1)
        df.dropna(inplace=True)
        metrics = PerformanceMetrics(df['strategy_returns'])
        metrics.calculate_metrics()
        logging.info("Backtesting completed successfully")
        return metrics
    except Exception as e:
        logging.error(f"Error during backtesting: {str(e)}")
        return None
