from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.product import product_router

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)
#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process