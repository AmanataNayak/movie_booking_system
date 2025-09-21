import mlflow
from fastapi import HTTPException
from cache import Cache

model_cache = Cache()

MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


def load_model_from_registry(model_name: str):
    """
        Loads a model from the MLflow registry.
        Checks cache first, otherwise downloads and caches the model.
    """
    model_uri = f"models:/{model_name}/1"

    model = model_cache.get(model_uri)
    if model:
        return model

    try:
        print(f"Loading model '{model_name}' from registry: {model_uri}")
        loaded_model = mlflow.pyfunc.load_model(model_uri)
        model_cache.set(model_uri, loaded_model)
        return loaded_model
    except mlflow.exceptions.MlflowException as me:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{model_name}' not found. Error: {me}"
        )

