from fastapi import FastAPI
from routes.register_route import router

app = FastAPI()
app.include_router(router, prefix="/api/auth", tags=["auth"])


