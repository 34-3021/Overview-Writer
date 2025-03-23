from fastapi import FastAPI
from routers import auth
from database import engine
from models.user import User

User.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
