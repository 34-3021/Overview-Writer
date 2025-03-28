from fastapi import FastAPI, Depends
from routers import auth, files, document
from database import engine
from models.user import User
from fastapi.middleware.cors import CORSMiddleware
from security import get_current_user

User.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

app.include_router(
    files.router,
    prefix="/files",
    tags=["Files"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    document.router,
    prefix="/documents",
    tags=["Documents"],
    dependencies=[Depends(get_current_user)]  # 保持安全验证一致
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=11451)
