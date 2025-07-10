
from dataclasses import dataclass
from typing import TypeVar
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base
from app.models import User, Company, Contact
from app.config import setup_log


log = setup_log(__name__)

T = TypeVar("T", bound="Base")


@dataclass
class BaseDAO():
    """Base class for getting data from the database

        Args:
            model: (DeclarativeBase): SQLalchemy model. Default = None
    """
    model: DeclarativeBase = None

    @classmethod
    async def get_all(cls, session_db: AsyncSession) -> list[T]:
        """Retrieve all unique instances of the model from the database asynchronously. 

        Args:
            session_db (AsyncSession): The SQLAlchemy asynchronous session.

        Returns:
            list[T]: list of all unique model instances found in the database.
        Returns an empty list if no records exist.
        """
        result = await session_db.scalars(select(cls.model))
        return result.unique().all()

    @classmethod
    async def get_details(cls, id: int | str, session_db: AsyncSession) -> T:
        """Retrieve instance of the model with all relations

        Args:
            id (int | str): ID instance of the model
            session_db (AsyncSession): The SQLAlchemy asynchronous session.

        Returns:
            T: model instances with all relations
        """
        result = await session_db.scalars(
            select(cls.model)
            .where(cls.model.id == id)
            .options(selectinload("*"))
        )
        return result.unique().one_or_none()
    
@dataclass
class UserDAO(BaseDAO):
    model = User

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


@dataclass
class ContactDAO(BaseDAO):
    model = Contact

    @classmethod
    async def get_user(cls, contact_id: int, session_db: AsyncSession):
        result = await session_db.execute(
            select(Contact)
            .where(Contact.id == contact_id)
            .options(selectinload(Contact.user))
        )
        contact = result.scalars().unique().one_or_none()
        if contact:
            return contact.user
        return None

    @classmethod
    async def get_company(cls, contact_id: int, session_db: AsyncSession):
        result = await session_db.scalars(
            select(Contact)
            .where(Contact.id == contact_id)
            .options(selectinload(Contact.company))
        )
        contact = result.unique().one_or_none()
        if contact:
            return contact.company
        return None

    @classmethod
    async def get_info(cls, contact_id: int, session_db: AsyncSession):
        result = await session_db.scalars(select(Contact).where(Contact.id == contact_id))

        return result.unique().one_or_none()
