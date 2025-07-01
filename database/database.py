__all__ = ["A_Session", "Base"]
from datetime import datetime
from sqlalchemy import Integer, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from config import config

DB_URL = config.get_db_url()

engine = create_async_engine(
    DB_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

A_Session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    @classmethod
    def from_dict(cls, data: dict):
        instance = cls()
        columns_dict = {c.name: getattr(instance, c.name)
                        for c in instance.__table__.columns}
        for key, value in data.items():
            if key.lower() in columns_dict:
                setattr(instance, key.lower(), value)
        return instance
