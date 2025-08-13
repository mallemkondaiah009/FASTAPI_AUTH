from fastapi import FastAPI, HTTPException, APIRouter
from models.user_model import User, UserResponse
from database.mongo_config import collection
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()
router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user:User):
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    try :
        hashed_password = pwd_context.hash(user.password)
        new_user = dict(user)
        new_user['password'] = hashed_password
        result = await collection.insert_one(new_user)
        return UserResponse(
            id=str(result.inserted_id),
            email=user.email,
            password=hashed_password
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register User: {str(e)}")


app.include_router(router)