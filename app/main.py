from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.product import product_router
from app.routes.cart import cart_router
from app.routes.order import order_router

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process