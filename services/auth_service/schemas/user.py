from models.user import UserRole
from pydantic import BaseModel, EmailStr, UUID4, ConfigDict

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    username: str
    email: EmailStr
    role: UserRole


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


