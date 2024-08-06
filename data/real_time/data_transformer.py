import pandas as pd
import numpy as np
import logging

class DataTransformer:
    @staticmethod
    def normalize_data(df):
        try:
            numeric_cols = df.select_dtypes(include=np.number).columns
            df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
            return df
        except Exception as e:
            logging.error(f"Failed to normalize data: {str(e)}")
            return df

    @staticmethod
    def add_features(df):
        try:
            df['price_change'] = df['price'].pct_change()
            df['volume_change'] = df['volume'].pct_change()
            df['moving_avg'] = df['price'].rolling(window=20).mean()
            df['exp_moving_avg'] = df['price'].ewm(span=20, adjust=False).mean()
            return df
        except Exception as e:
            logging.error(f"Failed to add features to data: {str(e)}")
            return df
