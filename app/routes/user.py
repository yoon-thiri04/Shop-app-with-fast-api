from fastapi import APIRouter, HTTPException,status, Depends
from app.models.user import UserRegister, UserLogin, UserResponse,UserUpdate,ChangePassword
from app.crud.user import register_user, get_user_by_email, update_user, change_password
from app.utils.authentication import generate_jwt_token, get_current_user
from app.utils.password import verify

router = APIRouter(prefix="", tags=["Authentication"])

@router.post("/register", response_model=dict)
async def register(user:UserRegister):
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="User with this mail already exists!")
    
    result = await register_user(user)

    return {
        "message":"User Register!"
    }
@router.post("/login", response_model=dict)
async def login(user:UserLogin):
    db_user = await get_user_by_email(user.email)

    if not db_user or not verify(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credential!")
    
    token =generate_jwt_token(
        {
            "id":db_user.id,
            "name":db_user.name,
            "email":db_user.email
        }
    )

    return {
        "message":"login success",
        "token":token
    }

@router.put("/update", response_model=dict)
async def update_user_info(update_data:UserUpdate, current_user= Depends(get_current_user)):
    user_id = current_user["id"]
    result = await update_user(user_id, update_data)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return {
        "message":"Successfully Updated!"
    }


@router.put("/change_pwd", response_model=dict)
async def change_pwd(update_data:ChangePassword, current_user=Depends(get_current_user)):
    user_id= current_user["id"]
    result = await change_password(user_id, update_data)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found!")
    
    return {"message":"Password Change Successfully!"}
