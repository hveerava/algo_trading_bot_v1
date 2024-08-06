import joblib
import pandas as pd
import logging

class ModelPrediction:
    def __init__(self, model_path, X_test):
        self.model = joblib.load(model_path)
        self.X_test = X_test

    def predict(self):
        try:
            predictions = self.model.predict(self.X_test)
            return pd.DataFrame({'prediction': predictions})
        except Exception as e:
            logging.error(f"Error during model prediction: {str(e)}")
            return pd.DataFrame()
