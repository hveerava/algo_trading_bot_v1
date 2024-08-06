import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import logging

class ModelTraining:
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def train(self):
        try:
            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
            model.fit(X_train, y_train)
            joblib.dump(model, 'trained_model.pkl')

            logging.info("Model training completed and saved to trained_model.pkl")
            return model
        except Exception as e:
            logging.error(f"Error during model training: {str(e)}")
            return None
