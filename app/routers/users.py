from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models import User
from app.schemes import CompanyRead, ContactRead, UserCreate, UserRead
from app.dao import UserDAO
from app.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users/"])


@router.get("/", summary="Gets all users", response_model=list[UserRead])
async def get_users(db_session: AsyncSession = Depends(get_db)):
    return await UserDAO.get_all(db_session)


@router.get("/{user_id}/companies", summary="Gets all user's companies", response_model=list[CompanyRead])
async def get_users_companies(user_id: int, db_session: AsyncSession = Depends(get_db)):
    return await UserDAO.get_companies(user_id, db_session)


@router.get("/{user_id}/contacts", summary="Gets all user's contacts", response_model=list[ContactRead])
async def get_users_contacts(user_id: int, db_session: AsyncSession = Depends(get_db)):
    return await UserDAO.get_contacts(user_id, db_session)


@router.get("/{user_id}", summary="Gets detail user's info", response_model=UserRead)
async def get_users_contacts(user_id: int, db_session: AsyncSession = Depends(get_db)):
    return await UserDAO.get_info(user_id, db_session)


@router.post(
    "/", 
    summary="Create new user", 
    response_model=UserRead, 
    status_code=status.HTTP_201_CREATED,
    )
async def create_users(user_data: UserCreate, db_session: AsyncSession = Depends(get_db)):
    existing_user = await db_session.execute(
        select(User).where(
            (User.username == user_data.username) | 
            (User.email == user_data.email)
        )
    )
    if existing_user.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    user_orm = User(**user_data.model_dump())
    hashed_password = get_password_hash(user_data.password)
    user_orm.hash_password = hashed_password
    db_session.add(user_orm)
    await db_session.commit()
    await db_session.refresh(user_orm)
    
    return user_orm

