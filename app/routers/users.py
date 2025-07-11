from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models import User
from app.schemas import UserCreate, UserFullResponse, UserResponse, UserUpdate
from app.database.dao import UserDAO


router = APIRouter(prefix="/users", tags=["users/"])


@router.get("/", summary="Gets all users", response_model=list[UserResponse])
async def get_users(db_session: AsyncSession = Depends(get_db)):
    return await UserDAO.get_all(db_session)


@router.get("/{user_id}", summary="Gets detail user's info", response_model=UserFullResponse)
async def get_user_info(user_id: int, db_session: AsyncSession = Depends(get_db)):
    user = await UserDAO.get_details(user_id, db_session)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with ID {user_id} not found"
    )


@router.post(
    "/",
    summary="Create new user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_users(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await UserDAO.create_new_record(user_data, db)
    if isinstance(result, User):
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=result
        )
    
@router.patch(
        "/{user_id}", 
        summary="Update user", 
        status_code=status.HTTP_200_OK, 
        response_model=UserResponse
    )
async def update_user(user_id: int, data: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await UserDAO.update_record(user_id, data, db)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error"
    )

@router.delete("/{user_id}", summary="Delete user", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await UserDAO.delete_record(user_id, db)
    if result:
        return {"status": "success", "deleted_id": user_id}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} not found",
    ) 


# @router.get("/{user_id}/companies", summary="Gets all user's companies", response_model=list[CompanyRead])
# async def get_users_companies(user_id: int, db_session: AsyncSession = Depends(get_db)):
#     return await UserDAO.get_companies(user_id, db_session)


# @router.get("/{user_id}/contacts", summary="Gets all user's contacts", response_model=list[ContactFullResponse])
# async def get_users_contacts(user_id: int, db_session: AsyncSession = Depends(get_db)):
#     return await UserDAO.get_contacts(user_id, db_session)