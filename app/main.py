from fastapi import FastAPI
from app.routers.cat_routers import cat_router
from app.routers.mission_routers import mission_router

app = FastAPI()

app.include_router(cat_router, prefix="/cat", tags=["Cat"])
app.include_router(mission_router, prefix="/mission", tags=["Mission"])
