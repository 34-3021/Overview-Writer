from .main import app
from .config import settings

__all__ = ["app", "settings"]

# Import all routers to register them
from .routers import embedding, vector_db, llm, document
