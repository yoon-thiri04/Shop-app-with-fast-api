from fastapi import APIRouter, HTTPException, Depends, status
from app.utils.authentication import get_current_user
from app.crud.cart import add_to_cart,remove_from_cart,view_cart,update_quantity
from app.models.cartItem import CartItem,QuantityUpdate
from app.models.cart import Cart
cart_router = APIRouter(prefix="/cart", tags=["Add to Cart"])

@cart_router.post("/add",response_model=dict)
async def add_to_cart_api(item: CartItem, current_user= Depends(get_current_user)):
    
    user_id = current_user["id"]

    result = await add_to_cart(item,user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't Add to Cart!")

    return {"message":"Successfully Add to Cart!"}


@cart_router.get("/", response_model=Cart)
async def view_cart_api(current_user: dict= Depends(get_current_user)):
    cart = await view_cart(current_user["id"])
    
    if cart["items"] == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart with that user not found!")
    
    return Cart.from_mongo(cart)

@cart_router.delete("/item/{product_id}", response_model=dict)
async def remove_from_cart_api(product_id:str, current_user:dict = Depends(get_current_user)):
    result = await remove_from_cart(current_user["id"], product_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail="Cart item with that username not found!")
    
    return {"message":"Succesfully Removed the item!"}

@cart_router.put("/item/{product_id}", response_model=dict)
async def update_quantity_api(product_id:str,quantity_update:QuantityUpdate, current_user:dict = Depends(get_current_user)):
    result = await update_quantity(current_user["id"],product_id, quantity_update)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")
    
    return {"message":"Successfully Updated the quantity of an item"}