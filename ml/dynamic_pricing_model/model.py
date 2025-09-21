import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

def train_model(X_train: pd.DataFrame, y_train: pd.Series, params: dict):
    """Trains a RandomForestRegressor model."""
    print(f"Training model with parameters: {params}")
    model = RandomForestRegressor(**params)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series):
    """Evaluates the model and prints the metrics."""
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"-> Mean Squared Error: {mse:.4f}")
    print(f"-> R-squared: {r2:.4f}")

def save_model(model, path: str):
    """Saves the trained model to the specified path."""
    print(f"Saving model to {path}...")
    joblib.dump(model, path)
    print("Model saved successfully.")