from fastapi import HTTPException,status
from app.models.order import OrderCreate,OrderResponse, OrderUpdate
from app.models.orderItem import OrderItem
from app.models.cart import Cart
from app.db import db
from bson import ObjectId
from datetime import datetime

orders_collection = db["orders"]
carts_collection = db["carts"]
products_collection = db["products"]
async def checkout(user_id: str, info:OrderCreate):
    cart = await carts_collection.find_one(
        {"user_id":ObjectId(user_id)}
    )

    if not cart or not cart.get("items"):
        raise HTTPException(status_code=400, detail="Cart not found or Cart is empty")
    
    total_price = 0 
    order_items= []
    for item in cart["items"]:
        product = await products_collection.find_one(
            {"_id":item["product_id"]}
            
        )
        total_price += product["price"] * item["quantity"]

        order_items.append({
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": product["price"]  # Store price at time of purchase
        })

    
    order = {
        "user_id":ObjectId(user_id),
        "items":order_items,
        "total_price":total_price,
        "status":"pending",
        "address":info.address.dict(),
        "phone":info.phone,
        "created_at": datetime.now(),
        "updated_at":datetime.now()
    }

    result = await orders_collection.insert_one(order)
    await carts_collection.delete_one(
        {"user_id":ObjectId(user_id)}
    )

    return True

async def view_orders(user_id:str):
    orders = await orders_collection.find({
        "user_id":ObjectId(user_id)
    }).to_list()
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orders with this user had not been placed!")
    return orders

async def view_order(order_id:str):
    order = await orders_collection.find_one(
        {"_id":ObjectId(order_id)}
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
    
    return order

async def update_order(order_id:str, update_data:OrderUpdate):
    result = await orders_collection.update_one(
        {"_id":ObjectId(order_id)},
        {"$set":update_data.model_dump(exclude_unset=True)}
    )

    return result.modified_count > 0

async def delete_order(order_id:str):
    result =await orders_collection.delete_one(
        {"_id":ObjectId(order_id)}
    )
    return result.deleted_count>0