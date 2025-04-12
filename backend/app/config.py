from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALGO_BASE_URL: str = "http://localhost:8001"  # 算法后端地址
    
settings = Settings()
