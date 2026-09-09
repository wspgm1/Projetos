from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import User, get_db
from .schemas import LoginRequest, TokenResponse, UserResponse
from .security import create_access_token, verify_password
from .dependencies import current_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not user.is_active or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    return {"access_token": create_access_token(user.username), "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(current_user)):
    return user
