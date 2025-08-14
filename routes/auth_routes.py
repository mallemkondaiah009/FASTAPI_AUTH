from fastapi import FastAPI, HTTPException, APIRouter
from models.user_model import User, UserResponse, UserUpdate
from database.mongo_config import collection
from passlib.context import CryptContext
from bson import ObjectId


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

@router.put("/update-user/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    try:
        # Validate user_id as a valid ObjectId
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID format")
        
        # Prepare update data - only include fields that were actually provided
        update_data = user_update.dict(exclude_unset=True)
        
        # Check if there's anything to update
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update")
        
        # Hash password if provided
        if "password" in update_data:
            update_data["password"] = pwd_context.hash(update_data["password"])
        
        # Update user in MongoDB
        result = await collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Safely construct response with error handling
        return UserResponse(
            id=str(result["_id"]),
            email=result.get("email", ""),
            username=result.get("username", "")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")
    
@router.get("/get-users", response_model=list[UserResponse])
async def get_users():
    try:
        users=[]
        async for user in collection.find():
            users.append(UserResponse(
                id=str(user["_id"]),
                username=user['username'],
                email=user['email']
            ))
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve users: {str(e)}")
    
@router.get("/get-user/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID format")
        
        user = await collection.find_one(
            {"_id": ObjectId(user_id)}
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=str(user["_id"]),
            username=user["username"],
            email=user["email"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {str(e)}")
    
@router.delete("/delete-user/{user_id}")
async def delete_user(user_id: str):
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID format")
        
        result = await collection.delete_one(
            {"_id": ObjectId(user_id)}
        )
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")       
app.include_router(router)