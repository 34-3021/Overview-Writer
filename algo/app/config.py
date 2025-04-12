from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    chroma_host: str = "http://localhost"
    chroma_port: int = 8000
    chroma_path: str = "../../chroma"

    query_model: str = "bge-m3"
    query_api_base: str = "http://10.176.64.152:11435/v1"
    query_api_key: str = "API_KEY_IS_NOT_NEEDED"

    embedding_model: str = "bge-m3"
    embedding_api_base: str = "http://10.176.64.152:11435/v1/embeddings"

    llm_model: str = "qwen2.5:7b"
    llm_api_base: str = "http://10.176.64.152:11434/v1/chat/completions"
    
    # class Config:
    #     env_file = ".env"

settings = Settings()
