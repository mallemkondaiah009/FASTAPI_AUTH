from fastapi import FastAPI
from routes.auth_routes import router

app = FastAPI()
app.include_router(router, prefix="/api/auth", tags=["auth"])


