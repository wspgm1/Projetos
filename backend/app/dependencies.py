from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from .database import User, RevokedToken, get_db
from .security import decode_access_token

bearer = HTTPBearer()
ROLES = {"admin", "manager", "employee"}


def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(credentials.credentials)
        jti = payload.get("jti")
        username = payload.get("sub")
        if not jti or not username:
            raise ValueError("Token incompleto")
        if db.query(RevokedToken).filter(RevokedToken.jti == jti).first():
            raise ValueError("Token revogado")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido, expirado ou revogado")

    user = db.query(User).filter(User.username == username, User.is_active.is_(True)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado ou inativo")
    return user


def require_roles(*roles: str):
    invalid = set(roles) - ROLES
    if invalid:
        raise ValueError(f"Perfis inválidos: {', '.join(sorted(invalid))}")

    def checker(user: User = Depends(current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão para esta operação")
        return user

    return checker

admin_required = require_roles("admin")
manager_required = require_roles("admin", "manager")
