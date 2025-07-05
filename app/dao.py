
from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Company, Contact


# @dataclass
# class BaseDAO():
#     model: DeclarativeBase = None

#     @classmethod
#     async def get_all(cls, session_db: AsyncSession):
#         result = await session_db.execute(select(cls.model).options(

#         ))
#         return result.scalars().all()

@dataclass
class UserDAO():
    model = User

    @classmethod
    async def get_all(cls, session_db: AsyncSession):
        result = await session_db.scalars(select(cls.model))
        return result.unique().all()

    @classmethod
    async def get_companies(cls, user_id: int, session_db: AsyncSession):
        result = await session_db.scalars(select(Company).where(Company.user_id == user_id))
        return result.unique().all()

    @classmethod
    async def get_contacts(cls, user_id: int, session_db: AsyncSession):
        result = await session_db.scalars(select(Contact).where(Contact.user_id == user_id))
        return result.unique().all()

    @classmethod
    async def get_info(cls, user_id: int, session_db: AsyncSession):
        result = await session_db.scalars(select(User).where(User.id == user_id))
        return result.unique().one_or_none()
