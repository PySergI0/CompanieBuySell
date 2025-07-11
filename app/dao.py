from dataclasses import dataclass
import re
from typing import TypeVar
from pydantic import BaseModel
from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database import Base
from app.models import User, Company, Contact
from app.config import setup_log
from app.security import get_password_hash


log = setup_log(__name__)

T = TypeVar("T", bound="Base")


@dataclass
class BaseDAO():
    """Base class for getting data from the database

        Args:
            model: (DeclarativeBase): SQLalchemy model. Default = None
    """
    model: Base = None

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
    
    @classmethod
    async def create_new_record(cls, data: BaseModel, session_db: AsyncSession):
        """Created new object in the DB"""
        try:
            model = cls.model(**data.model_dump())
            session_db.add(model)
            await session_db.commit()
            await session_db.refresh(model)
            return model
        except IntegrityError as e:
            log.debug(f"Error added {e}")
            error_msg = str(e.orig)
            detail_match = re.search(r'DETAIL:\s*(.*)', error_msg)
            detail = detail_match.group(1) if detail_match else "Неизвестная ошибка уникальности"
            log.debug(f"Error added object: {detail}")
            return {
                "error": "duplicate_key",
                "message": "Нарушение уникальности данных",
                "detail": " ".join(detail.split()[:-3])
            }
        
    @classmethod
    async def delete_record(cls, id: int, session_db: AsyncSession) -> bool:
        result = await session_db.execute(delete(cls.model).where(cls.model.id == id))
        await session_db.commit()
        return result.rowcount > 0
    
    @classmethod
    async def update_record(cls, id: int, data: BaseModel, session_db: AsyncSession):
        update_values = {k: v for k, v in data.model_dump().items() if v is not None}
        try:
            await session_db.execute(
                update(cls.model)
                .where(cls.model.id == id)
                .values(update_values)
            )
            updated_obj = await session_db.get(cls.model, id)
            await session_db.commit()
            log.debug(f"Updating {cls.__name__} id={id} with values: {update_values}")
            return updated_obj
        except Exception as e:
            log.error(f"Error updating: {e}")
            return None
        

@dataclass
class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def create_new_record(cls, data: BaseModel, session_db: AsyncSession):
        try:
            model = cls.model(**data.model_dump())
            hashed_password = get_password_hash(data.password)
            model.hash_password = hashed_password
            session_db.add(model)
            await session_db.commit()
            await session_db.refresh(model)
            return model
        except IntegrityError as e:
            log.debug(f"Error added {e}")
            error_msg = str(e.orig)
            detail_match = re.search(r'DETAIL:\s*(.*)', error_msg)
            detail = detail_match.group(1) if detail_match else "Неизвестная ошибка уникальности"
            return {
                "error": "duplicate_key",
                "message": "Нарушение уникальности данных",
                "detail": detail
            }

    @classmethod
    async def get_companies(cls, user_id: int, session_db: AsyncSession):
        result = await session_db.scalars(select(Company).where(Company.user_id == user_id))
        return result.unique().all()

    @classmethod
    async def get_contacts(cls, user_id: int, session_db: AsyncSession):
        result = await session_db.scalars(select(Contact).where(Contact.user_id == user_id))
        return result.unique().all()

    # @classmethod
    # async def get_info(cls, user_id: int, session_db: AsyncSession):
    #     result = await session_db.scalars(select(User).where(User.id == user_id))
    #     return result.unique().one_or_none()


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

@dataclass
class CompanyDAO(BaseDAO):
    model = Company

