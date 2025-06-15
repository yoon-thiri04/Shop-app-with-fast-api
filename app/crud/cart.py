from app.models.cart import Cart
from app.models.cartItem import CartItem, QuantityUpdate
from bson import ObjectId
from app.db import db
from fastapi import HTTPException

carts_collection= db['carts']

async def add_to_cart(cartItem: CartItem, user_id:str):
    add_to_cart_items = cartItem.model_dump()
    
    cart = await carts_collection.find_one({
        "user_id":ObjectId(user_id)
    }) 

    if cart:
        for item in cart["items"]:
            if str(item['product_id']) == add_to_cart_items['product_id']:
                item['quantity'] += add_to_cart_items['quantity']
                break

        else:
            cart["items"].append(
                {
                    "product_id":ObjectId(add_to_cart_items['product_id']),
                    "quantity":add_to_cart_items['quantity']
                }
            )
        await carts_collection.update_one({"user_id":ObjectId(user_id)},
                                          {"$set":{"items":cart["items"]}})
    else:
        await carts_collection.insert_one(
            {
                "user_id":ObjectId(user_id),
                "items":[{"product_id": ObjectId(add_to_cart_items['product_id']),
            "quantity": add_to_cart_items['quantity']
            }]
             }
        )
    return True

async def view_cart(user_id:str):
    cart = await carts_collection.find_one(
        {"user_id":ObjectId(user_id)}
    )
    if not cart:
        return {"items":[]}

    return cart

async def remove_from_cart(user_id:str, product_id:str):
    
    result = await carts_collection.update_one(
        {"user_id":ObjectId(user_id)},
        {"$pull":{
            "items":{"product_id":ObjectId(product_id)}
            }
        }
    )

    return result.modified_count > 0

async def update_quantity(user_id:str, product_id:str,update_data:QuantityUpdate ):

    result = await db.carts.update_one(
    {
        "user_id": ObjectId(user_id),
        "items.product_id": ObjectId(product_id)
    },
    {
        "$set": {"items.$.quantity": update_data.quantity}
    }
)
    print(update_data.quantity)
    
    if result.modified_count == 0 :
        raise HTTPException(status_code=404, detail="Cart item not found or unchanged")
    
    return result.modified_count > 0