from fastapi import Depends, HTTPException, status
from app.utils.authentication import get_current_user

async def admin_required_api(current_user= Depends(get_current_user)):
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user