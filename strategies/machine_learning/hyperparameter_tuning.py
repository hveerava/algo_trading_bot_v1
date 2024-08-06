from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import joblib
import logging

class HyperparameterTuning:
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def tune_model(self):
        try:
            model = RandomForestClassifier()
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [10, 20],
                'min_samples_split': [2, 5]
            }
            grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy')
            grid_search.fit(self.X, self.y)
            best_model = grid_search.best_estimator_
            joblib.dump(best_model, 'best_model.pkl')

            logging.info("Hyperparameter tuning completed and best model saved to best_model.pkl")
            return best_model
        except Exception as e:
            logging.error(f"Error in hyperparameter tuning: {str(e)}")
            return None
