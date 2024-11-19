from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings


DB_URL = settings.DB_URL

if settings.MODE == "TEST":
    DB_URL = settings.TEST_DB_URL

engine = create_async_engine(DB_URL)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
