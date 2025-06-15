from pydantic import BaseModel
from typing import List,Optional
from app.models.cartItem import CartItem

class Cart(BaseModel):
    user_id : str
    items: List[CartItem] =[]
    @classmethod
    def from_mongo(cls, cart):
        items = [
        {
            **item,
            "product_id": str(item["product_id"])
        }
        for item in cart["items"]
        ]
        return cls(
            user_id=str(cart["user_id"]),
            items=items
        )

