from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from .config import DB_DSN

class Base(DeclarativeBase): pass

_engine = create_async_engine(DB_DSN, echo=False, future=True)
SessionLocal = async_sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)

def get_engine():
    return _engine
