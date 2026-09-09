from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=8, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    is_active: bool

class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=128)
    role: str = "employee"

class UserUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: str | None = None
    is_active: bool | None = None
