import chromadb
from chromadb.utils import embedding_functions
from config import settings

class VectorDB:
    def __init__(self):
        try:
            if settings.chroma_path:
                self.client = chromadb.PersistentClient(path=settings.chroma_path)
            else:
                self.client = chromadb.HttpClient(
                    host=settings.chroma_host,
                    port=settings.chroma_port,
                    settings=chromadb.Settings(anonymized_telemetry=False)
                )
            
            self.embedding_func = embedding_functions.DefaultEmbeddingFunction()
            # test the connection
            self.client.heartbeat()
            
        except Exception as e:
            raise ConnectionError(f"Failed to connect to ChromaDB: {str(e)}")
    
    def get_collection(self, name: str):
        return self.client.get_collection(
            name=name,
            embedding_function=self.embedding_func
        )
    
    def create_collection(self, name: str):
        return self.client.create_collection(
            name=name,
            embedding_function=self.embedding_func
        )

vector_db = VectorDB()
