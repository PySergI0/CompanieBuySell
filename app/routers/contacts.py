from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models import User
from app.schemas import CompanyRead, ContactFullResponse, UserCreate, UserResponse, ContactResponse
from app.dao import ContactDAO, UserDAO
from app.security import get_password_hash

router = APIRouter(prefix="/contacts", tags=["contacts/"])


@router.get("/", summary="Gets all contacts", response_model=list[ContactResponse])
async def get_contacts(db_session: AsyncSession = Depends(get_db)):
    return await ContactDAO.get_all(db_session)


@router.get("/{contact_id}", summary="Gets detail contact's info", response_model=ContactFullResponse)
async def get_contact_detail(contact_id: int, db_session: AsyncSession = Depends(get_db)):
    contact = await ContactDAO.get_details(contact_id, db_session)
    if contact:
        return contact
    raise HTTPException(
        status_code=404,
        detail="Contact not found"
    )





@router.get("/{contact_id}/user", summary="Gets contact's user", response_model=UserResponse)
async def get_contact_user(contact_id: int, db_session: AsyncSession = Depends(get_db)):
    return await ContactDAO.get_user(contact_id, db_session)


@router.get("/{contact_id}/company", summary="Gets contact's user", response_model=CompanyRead)
async def get_contact_company(contact_id: int, db_session: AsyncSession = Depends(get_db)):
    return await ContactDAO.get_company(contact_id, db_session)


