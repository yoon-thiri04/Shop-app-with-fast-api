from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class ProductCreate(BaseModel):
    name : str
    decription : Optional[str] = ""
    category : str
    price : float
    quantity_in_stock : int
    created_at : Optional[datetime] = datetime.now()
    updated_at : Optional[datetime] = datetime.now()

class ProductResponse(BaseModel):
    id : str
    name:str
    description:str
    category: str
    price: float
    quantity_in_stock :int
    created_at : datetime
    updated_at : datetime
    
    @classmethod
    def from_mongo(cls, product):
        return cls(
            id= str(product["_id"]),
            name= product["name"],
            description=product["description"],
            category= product["category"],
            price= product["price"],
            quantity_in_stock= product["quantity_in_stock"],
            created_at = product["created_at"],
            updated_at = product["updated_at"]
        )

class ProductUpdate(BaseModel):
    name : Optional[str] = None
    description: Optional[str] = ""
    category : Optional[str] = None
    price : Optional[str]= None
    quantity_in_stock: Optional[str] =None
    updated_at : Optional[datetime] = datetime.now()


