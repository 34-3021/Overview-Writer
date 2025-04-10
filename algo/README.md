
# Algorithm Backend

This service handles all AI-related functionality including:
- Vector database operations
- Document embedding
- LLM interactions
- Content generation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start ChromaDB vector database:
```bash
chroma run --path ./chroma_data --port 8002
```

3. Start the algorithm backend:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

## Environment Variables

Create a `.env` file to override default settings:
```
CHROMA_HOST=localhost
CHROMA_PORT=8002
EMBEDDING_MODEL=bge-m3
RERANK_MODEL=bge-reranker-v2-m3
LLM_MODEL=deepseek-v3
LLM_API_BASE=http://localhost:11452/v1
```

## API Documentation

Access after starting server:  
`http://localhost:8001/docs`  
`http://localhost:8001/redoc`