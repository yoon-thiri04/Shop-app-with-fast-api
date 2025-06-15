from pydantic import BaseModel

class CartItem(BaseModel): 
    product_id :str
    quantity :int

class QuantityUpdate(BaseModel):
    quantity:int