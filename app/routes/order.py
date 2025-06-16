from fastapi import APIRouter, HTTPException, status, Depends
from app.models.order import  OrderResponse, OrderUpdate,OrderCreate
from app.utils.authentication import get_current_user
from app.utils.dependencies import admin_required_api
from app.crud.order import checkout,view_order,view_orders,view_orders_by_admin,update_order,delete_order

order_router = APIRouter(prefix="/orders", tags=["Order"])

@order_router.post("/checkout",response_model=dict)
async def checkout_api(info:OrderCreate,current_user:dict= Depends(get_current_user)):
    user_id = current_user["id"]

    result = await checkout(user_id,info)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot Inserted")
    
    return {"message":"Successfully Placed an order!"}

@order_router.get("/",response_model=list[OrderResponse])
async def view_orders_api(current_user:dict = Depends(get_current_user)):
    user_id = current_user["id"]
    if current_user.get("is_admin"):
        orders = await view_orders_by_admin()

    else:
        orders = await view_orders(user_id)
    return [OrderResponse.from_mongo(order) for order in orders]

@order_router.get("/{order_id}", response_model=OrderResponse)
async def view_order_api(order_id:str, current_user:dict= Depends(get_current_user)):
    order = await view_order(order_id)
    return OrderResponse.from_mongo(order)

@order_router.put("/{order_id}", response_model=dict)
async def update_order_api(order_id:str,update_data: OrderUpdate, current_user:dict= Depends(admin_required_api)):
    result = await update_order(order_id,update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found!")
    
    return {"message":"Successfully updated"}

@order_router.delete("/{order_id}", response_model=dict)
async def delete_order_api(order_id:str,current_user:dict = Depends(admin_required_api)):
    result = await delete_order(order_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order Not found!")
    
    return {"message":"Successfully Deleted!"}