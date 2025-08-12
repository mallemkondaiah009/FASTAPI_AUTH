from fastapi import FastAPI, HTTPException, APIRouter
from models.user_model import User
from database.mongo_config import collection
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()
router = APIRouter()

@router.post("/register", response_model=User)
async def register_user(user:User):
    existing_user = collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = dict(user)
    new_user['password'] = hashed_password
    resp = collection.insert_one(new_user)
    return {
        "id": str(resp.inserted_id),
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }

app.include_router(router)