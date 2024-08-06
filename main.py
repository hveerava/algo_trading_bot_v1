import sys
import os
sys.path.insert(0, '/Users/harshithaveeravalli/Desktop/projs/algo_trading_bot_v2/data/real_time/scraping')


from data.real_time.data_fetcher import DataFetcher
from data.real_time.data_cleaner import DataCleaner
from data.real_time.data_transformer import DataTransformer
from data.storage.database import Database
from data.storage.cache import Cache
from strategies.mean_reversion import MeanReversionStrategy
from strategies.arbitrage import ArbitrageStrategy
from strategies.momentum import MomentumStrategy
from strategies.pairs_trading import PairsTradingStrategy
from backtesting.backtest import backtest_strategy
from execution.transaction_logger import TransactionLogger
from execution.risk_management import RiskManagement

def main():
    stock_base_url = 'FILL URL HERE'
    forex_base_url = 'FILL URL HERE'
    db_path = 'trading_bot.db'
    cache_path = 'cache.json'
    log_file = 'trading.log'
    max_drawdown = 0.1
    max_position_size = 10000

    data_fetcher = DataFetcher(stock_base_url, forex_base_url)
    stock_data = data_fetcher.get_stock_data('AAPL')
    forex_data = data_fetcher.get_forex_data('EUR/USD')

    cleaned_stock_data = DataCleaner.clean_stock_data(stock_data)
    cleaned_forex_data = DataCleaner.clean_forex_data(forex_data)

    transformed_stock_data = DataTransformer.add_features(cleaned_stock_data)
    transformed_stock_data = DataTransformer.normalize_data(transformed_stock_data)

    cache = Cache(cache_path)
    cache.save({
        'stock_data': transformed_stock_data.to_dict(orient='records'),
        'forex_data': cleaned_forex_data.to_dict(orient='records')
    })

    db = Database(db_path)
    if transformed_stock_data.empty:
        raise ValueError("Transformed stock data is empty. Cannot proceed with database insertion.")

    db.insert_stock_data(transformed_stock_data.to_dict(orient='records')[0])
    db.insert_forex_data(cleaned_forex_data.to_dict(orient='records')[0])

    momentum_strategy = MomentumStrategy(transformed_stock_data)
    momentum_signals = momentum_strategy.execute()
    
    mean_reversion_strategy = MeanReversionStrategy(transformed_stock_data)
    mean_reversion_signals = mean_reversion_strategy.execute()
    
    pairs_trading_strategy = PairsTradingStrategy(transformed_stock_data, cleaned_forex_data)
    pairs_trading_signals = pairs_trading_strategy.execute()
    
    arbitrage_strategy = ArbitrageStrategy(transformed_stock_data, cleaned_forex_data)
    arbitrage_opportunities = arbitrage_strategy.execute()

    backtest_strategy(mean_reversion_signals)

    risk_manager = RiskManagement(max_drawdown, max_position_size)
    risk_manager.check_drawdown(portfolio_value=50000)
    risk_manager.check_position_size(position_size=5000)

    logger = TransactionLogger(log_file)
    logger.log_trade({'symbol': 'AAPL', 'action': 'BUY', 'price': 150})
    logger.log_error('Sample error message')

if __name__ == '__main__':
    main()