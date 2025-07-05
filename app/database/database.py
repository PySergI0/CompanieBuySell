__all__ = ["A_Session", "Base", "BaseComment"]
from datetime import datetime
from sqlalchemy import Integer, Text, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.config import config

DB_URL = config.get_db_url()

engine = create_async_engine(
    DB_URL,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=300,
    pool_pre_ping=True,
    echo=False,
)

A_Session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    async with A_Session() as session:
        try:
            yield session
        finally:
            await session.close()


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now())

    @classmethod
    def from_dict(cls, data: dict):
        instance = cls()
        columns_dict = {c.name: getattr(instance, c.name)
                        for c in instance.__table__.columns}
        for key, value in data.items():
            if key.lower() in columns_dict:
                setattr(instance, key.lower(), value)
        return instance


class BaseComment(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text)
