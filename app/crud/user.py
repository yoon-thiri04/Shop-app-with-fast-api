from app.db import db
from app.models.user import UserLogin,UserRegister,UserResponse, UserUpdate, ChangePassword
from fastapi import HTTPException,status
from app.utils.password import hash,verify
from bson import ObjectId

users_collection= db['users']

async def register_user(user:UserRegister):

    hashed_password = hash(user.password)

    user_data = user.model_dump()
    
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    user_data['password']= hashed_password
    user_data.pop('confirm_password', None)
    result = await users_collection.insert_one(
        user_data
    )
    
    return UserResponse(id=str(result.inserted_id),**user_data)

async def get_user_by_email(email:str):
    user = await users_collection.find_one(
        {"email":email}
    )
    if user:
        return UserResponse(id=str(user["_id"]), **user)
    return None

async def update_user(user_id: str, update_data: UserUpdate):
    
    result = await users_collection.update_one(
        {"_id":ObjectId(user_id)},
        {"$set":update_data.model_dump(exclude_unset=True)}
    )
    return result.modified_count>0

async def change_password(user_id:str, update_data:ChangePassword):
    user = await users_collection.find_one(
        {"_id":ObjectId(user_id)}
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    if not verify(update_data.old_password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect!")
    
    if update_data.password != update_data.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New Passwords do not match!")
    
    hashed_password= hash(update_data.password)

    result = await users_collection.update_one(
        {"_id":ObjectId(user_id)},
        {"$set":{"password":hashed_password}}
    )

    return result.modified_count>0