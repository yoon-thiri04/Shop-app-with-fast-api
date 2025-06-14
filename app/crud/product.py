from fastapi import HTTPException,status
from app.db import db
from bson import ObjectId
from app.models.product import ProductCreate, ProductResponse, ProductUpdate
from pymongo.errors import PyMongoError
products_collection = db["products"]

async def create_product(prodcut:ProductCreate):
    try:
        await products_collection.insert_one( prodcut.model_dump())
        return True
    except PyMongoError as e:
        
        print(f"Error inserting product: {e}")
        return False



async def get_products():
    products= await products_collection.find().to_list()
    return products

async def get_product(product_id: str):
    product = await products_collection.find_one(
        {"_id":ObjectId(product_id)}
    )
    return product

async def update_product(product_id:str,update_data: ProductUpdate):
    result = await products_collection.update_one(
        {"_id":ObjectId(product_id)},
        {"$set":update_data.model_dump(exclude_unset=True)}
    )

    return result.modified_count>0