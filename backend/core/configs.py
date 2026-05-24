from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


DBBaseModel = declarative_base()

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str 
    
    JWT_SECRET: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    

    class Config:
        env_file = ".env" 
        case_sensitive = True


settings = Settings()