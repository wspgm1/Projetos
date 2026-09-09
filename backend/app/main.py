from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, User, engine, SessionLocal
from .routes_auth import router as auth_router
from .security import hash_password

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == settings.admin_username).first():
            db.add(User(username=settings.admin_username, password_hash=hash_password(settings.admin_password), role="admin"))
            db.commit()
    finally:
        db.close()

@app.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok"}
