from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime
from app.models.orderItem import OrderItem


class Address(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str


class AddressUpdate(BaseModel):
    street : Optional[str]=None
    city: Optional[str] =None
    state : Optional[str] =None
    postal_code: Optional[str] =None
    country: Optional[str] =None

class OrderCreate(BaseModel):
    address: Address
    phone : str

class OrderResponse(BaseModel):
    id: str
    user_id : str
    items: List[OrderItem]
    total_price: float
    status: str
    address: Address
    phone: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_mongo(cls,order):
        items = [
        {
            **item,
            "product_id": str(item["product_id"])
        }
        for item in order["items"]
        ]
        return cls(
            id= str(order["_id"]),
            user_id= str(order["user_id"]),
            items= items,
            total_price= order["total_price"],
            status = order["status"],
            address = order["address"],
            phone= order["phone"],
            created_at= order["created_at"],
            updated_at= order["updated_at"]
        )
    
    
class OrderUpdate(BaseModel):
    status: Optional[str] = None
    address: Optional[AddressUpdate] =None
    phone: Optional[str] =None
    updated_at: Optional[datetime] = datetime.now()