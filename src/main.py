from fastapi import FastAPI
from .interfaces.api.routers.price_router import router as price_router

app = FastAPI(title='price')
app.include_router(price_router)
