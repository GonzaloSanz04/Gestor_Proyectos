from src.routers.health import router as health_router 
from fastapi import FastAPI

app = FastAPI()
app.include_router(health_router)