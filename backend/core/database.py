from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.configs import settings
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.__all_models import *

engine: AsyncEngine = create_async_engine(settings.DB_URL)


SessionLocal: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)