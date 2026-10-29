
from fastapi import FastAPI

from src.routers.auth import router as registro
from src.routers.health import router as health_router 

app = FastAPI()
app.include_router(health_router)
app.include_router(registro)