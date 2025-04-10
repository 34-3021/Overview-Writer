from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    embedding, 
    vector_db, 
    llm,
    document
)
from config import settings

app = FastAPI(
    title="Algorithm Backend API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(embedding.router, prefix="/embedding", tags=["Embedding"])
app.include_router(vector_db.router, prefix="/vector-db", tags=["Vector Database"])
app.include_router(llm.router, prefix="/llm", tags=["LLM"])
app.include_router(document.router, prefix="/document", tags=["Document Processing"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
