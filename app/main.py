import logging
from sqlite3 import OperationalError

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.database import engine, Base
from app.routers import auth, user, operator, restaurant
from app.core.config import settings

try:
    Base.metadata.create_all(bind=engine)
except OperationalError:
    logging.info("Cannot connect to database")


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Smart Menu Application with JWT Authentication",
    version="1.0.0",
    debug=True
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(operator.router, prefix="/api")
app.include_router(restaurant.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)