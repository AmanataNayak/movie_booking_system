import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import mlflow

def train_model(X_train: pd.DataFrame, y_train: pd.Series, params: dict):
    """Trains a RandomForestRegressor model."""
    print(f"Training model with parameters: {params}")
    model = RandomForestRegressor(**params)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series):
    """Evaluates the model and prints the metrics."""
    print("Evaluating model...")
    y_pred = model.predict(X_test.to_numpy())
    metrics = {
        "mse": mean_squared_error(y_test.to_numpy(), y_pred),
        "r2": r2_score(y_test.to_numpy(), y_pred)
    }

    print(f"-> Mean Squared Error: {metrics['mse']:.4f}")
    print(f"-> R-squared: {metrics['r2']:.4f}")
    return metrics

def save_model_to_registry(model, model_name: str, config: dict, metrics: dict):
    """Logs the model, parameters, and metrics to the MLflow Model Registry."""
    print(f"Saving model '{model_name}' to the MLflow Registry...")
    mlflow.set_tracking_uri("http://127.0.0.1:5000")

    with mlflow.start_run():
        mlflow.log_params(config['model_params'])
        mlflow.log_metrics(metrics)

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name=model_name
        )

    print("Model saved successfully to register.")