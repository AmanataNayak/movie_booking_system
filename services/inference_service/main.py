from fastapi import FastAPI, HTTPException
import numpy as nd
from schemas.DynamicPricing import PredictionRequest
from utility.get_models import load_model_from_registry
import pandas as pd

app = FastAPI(
    title="Central Inference Service",
    description="A single service to serve predictions for any ML model in the registry."
)

@app.post("/predictions/{model_name}")
def inference(model_name: str, request: PredictionRequest):
    """
        Generic prediction endpoint.
        Loads the specified model and returns its prediction.
    """
    model = load_model_from_registry(model_name)
    try:
        input_df = pd.DataFrame(**request.dataframe_split)
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid input data format. Error: {e}")

    predictions = model.predict(input_df)
    return {"predictions": predictions.tolist()}

@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
