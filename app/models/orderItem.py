from pydantic import BaseModel
from typing import Optional

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class OrderItemResponse(BaseModel):
    id : str
    product_id : str
    quantity: str
    price : str

    @classmethod
    def from_mongo(cls, orderitem):
        return cls(
            id= str(orderitem["_id"]),
            product_id = str(orderitem["product_id"]),
            quantity= orderitem["quantity"],
            price =orderitem["price"]
        )