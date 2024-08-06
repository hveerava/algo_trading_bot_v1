import pandas as pd
import numpy as np
import logging

class FeatureEngineering:
    @staticmethod
    def create_features(df):
        try:
            df['price_change'] = df['price'].pct_change()
            df['volume_change'] = df['volume'].pct_change()
            df['moving_avg'] = df['price'].rolling(window=20).mean()
            df['volatility'] = df['price'].rolling(window=20).std()
            df['momentum'] = df['price'] - df['price'].shift(14)
            df['relative_strength'] = df['price'].pct_change(14)
            df.fillna(0, inplace=True)
            return df
        except Exception as e:
            logging.error(f"Error in feature engineering: {str(e)}")
            return pd.DataFrame()