from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import  OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from security import verify_password, create_access_token
from database import  get_db
import services
from schemas.user import *
from iam import get_current_user, TokenData

app = FastAPI()

ouath2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=str(user.email))
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Email already register"
        )
    return services.create_user(db, user)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = services.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        # type UUID can't be serialize into json
        data={"sub": str(user.id), "username": user.username, "role": user.role.value}
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user = services.get_user_by_username(db, current_user.username)
    return current_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
