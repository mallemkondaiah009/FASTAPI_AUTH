from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str | None = None
    username: str | None = None
    email: EmailStr | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


