from pydantic import BaseModel

class PredictionRequest(BaseModel):
    dataframe_split: dict

    