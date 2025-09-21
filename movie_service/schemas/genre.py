from pydantic import BaseModel, ConfigDict, UUID4

class GenerCreate(BaseModel):
    name: str

class GenreOut(GenerCreate):
    id: UUID4
    model_config = ConfigDict(from_attributes=True)



