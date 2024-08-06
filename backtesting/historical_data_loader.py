import pandas as pd
import logging

class HistoricalDataLoader:
    @staticmethod
    def load_data(file_path):
        try:
            df = pd.read_csv(file_path, parse_dates=['timestamp'])
            logging.info(f"Data loaded successfully from {file_path}")
            return df
        except Exception as e:
            logging.error(f"Error loading data from {file_path}: {str(e)}")
            return pd.DataFrame()
