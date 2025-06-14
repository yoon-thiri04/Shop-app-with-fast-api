from app.crud.product import create_product,get_product, get_products, update_product
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.product import ProductCreate,ProductResponse,ProductUpdate
from app.utils.authentication import get_current_user
from app.utils.dependencies import admin_required_api

product_router = APIRouter(prefix="/products", tags=["Products"])

@product_router.post("/", response_model=dict)
async def create_product_api(product:ProductCreate, current_user= Depends(admin_required_api)):
    await create_product(product)
    return {"message":"Product Created!"}


@product_router.get("/", response_model=list[ProductResponse])
async def get_products_api(current_user:dict=Depends(get_current_user)):
    products =await get_products()
    return [ProductResponse.from_mongo(product) for product in products]


@product_router.get("/{product_id}", response_model=ProductResponse)
async def get_product_api(product_id:str,current_user:dict= Depends(get_current_user)):
    product = await get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail= "Product Not Found!") 
    return ProductResponse.from_mongo(product)

@product_router.put("/{product_id}",response_model=dict)
async def update_product_api(product_id:str, update_data:ProductUpdate,current_user:dict= Depends(admin_required_api)):
    result = await update_product(product_id, update_data)
    if not result:
        raise HTTPException(status_code=404,detail="Product Not Found!")
    return {"message":"Product Updated Successfully!"}
