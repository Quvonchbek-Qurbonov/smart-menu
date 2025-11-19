from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.utils.database import engine, Base
from app.routers import auth, menu, orders
from app.core.config import settings


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Smart Menu Application with JWT Authentication",
    version="1.0.0",
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(menu.router)
app.include_router(orders.router)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to Smart Menu API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }