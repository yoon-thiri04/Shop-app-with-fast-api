from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime
from app.models.orderItem import OrderItem

class OrderCreate(BaseModel):
    user_id: str
    item: List[OrderItem]
    total_amount : float
    status : str="pending"
    created_at : Optional[datetime] = datetime.now()
    updated_at : Optional[datetime] = datetime.now()

class OrderResponse(BaseModel):
    id: str
    user_id : str
    item: List[OrderItem]
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_mongo(cls,order):
        return cls(
            id= str(order["_id"]),
            user_id= str(order["user_id"]),
            item= order["item"],
            total_amount= order["total_amount"],
            status = order["status"],
            created_at= order["created_at"],
            updated_at= order["updated_at"]
        )
    

