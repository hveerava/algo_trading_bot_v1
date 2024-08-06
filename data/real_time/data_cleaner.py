import pandas as pd
import logging

class DataCleaner:
    @staticmethod
    def clean_stock_data(data):
        try:
            df = pd.DataFrame([data])
            df['price'] = pd.to_numeric(df['price'].str.replace(',', ''), errors='coerce')
            df['volume'] = pd.to_numeric(df['volume'].str.replace(',', ''), errors='coerce')
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            logging.error(f"Failed to clean stock data: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def clean_forex_data(data):
        try:
            df = pd.DataFrame([data])
            df['exchange_rate'] = pd.to_numeric(df['exchange_rate'].str.replace(',', ''), errors='coerce')
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            logging.error(f"Failed to clean forex data: {str(e)}")
            return pd.DataFrame()
