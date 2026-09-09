from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from .database import User, RevokedToken, get_db
from .schemas import LoginRequest, TokenResponse, UserResponse, UserCreateRequest, UserUpdateRequest
from .security import create_access_token, verify_password, hash_password, decode_access_token
from .dependencies import current_user, admin_required

router = APIRouter(prefix="/auth", tags=["Autenticação"])
bearer = HTTPBearer()
VALID_ROLES = {"admin", "manager", "employee"}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not user.is_active or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    token, _, _ = create_access_token(str(user.id), user.role)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout", status_code=204)
def logout(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db), user: User = Depends(current_user)):
    try:
        payload = decode_access_token(credentials.credentials)
        jti = payload["jti"]
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc).replace(tzinfo=None)
        if not db.query(RevokedToken).filter(RevokedToken.jti == jti).first():
            db.add(RevokedToken(jti=jti, expires_at=exp, user_id=user.id))
            db.commit()
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(current_user)):
    return user

@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(data: UserCreateRequest, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    if data.role not in VALID_ROLES: raise HTTPException(status_code=400, detail="Perfil inválido")
    if db.query(User).filter(User.username == data.username).first(): raise HTTPException(status_code=409, detail="Usuário já existe")
    user = User(username=data.username, full_name=data.full_name, password_hash=hash_password(data.password), role=data.role)
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return db.query(User).order_by(User.id).all()

@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdateRequest, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if data.role is not None:
        if data.role not in VALID_ROLES: raise HTTPException(status_code=400, detail="Perfil inválido")
        user.role = data.role
    if data.full_name is not None: user.full_name = data.full_name
    if data.password is not None: user.password_hash = hash_password(data.password)
    if data.is_active is not None: user.is_active = data.is_active
    db.commit(); db.refresh(user)
    return user

@router.delete("/users/{user_id}", status_code=204)
def deactivate_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(admin_required)):
    if user_id == admin.id: raise HTTPException(status_code=400, detail="O administrador não pode desativar a própria conta")
    user = db.query(User).filter(User.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user.is_active = False; db.commit()
