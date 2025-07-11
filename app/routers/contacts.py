from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models import Contact
from app.schemas import CompanyRead, ContactCreate, ContactFullResponse, ContactUpdate, UserCreate, UserFullResponse, UserResponse, ContactResponse
from app.dao import ContactDAO


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
        detail="Contact with ID {contact_id} not found"
    )

@router.post(
        "/",
        summary="Create new contact",
        status_code=status.HTTP_201_CREATED,
        response_model=ContactResponse,
    )
async def create_contact(contact_data: ContactCreate, db: AsyncSession = Depends(get_db)):
    result = await ContactDAO.create(contact_data, db)
    if isinstance(result, Contact):
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "duplicate_key",
                "message": "Нарушение уникальности данных",
                "detail": result
            }
        )


@router.patch(
        "/{contact_id}", 
        summary="Update contact", 
        status_code=status.HTTP_200_OK, 
        response_model=ContactResponse
    )
async def update_contact(contact_id: int, data: ContactUpdate, db: AsyncSession = Depends(get_db)):
    result = await ContactDAO.update_record(contact_id, data, db)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error"
    )


@router.delete("/{contact_id}", summary="Delete contact", status_code=status.HTTP_200_OK)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    result = await ContactDAO.delete_record(contact_id, db)
    if result:
        return {"status": "success", "deleted_id": contact_id}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Contact with id {contact_id} not found",
    ) 


# @router.get("/{contact_id}/user", summary="Gets contact's user", response_model=UserFullResponse)
# async def get_contact_user(contact_id: int, db_session: AsyncSession = Depends(get_db)):
#     user =  await ContactDAO.get_user(contact_id, db_session)
#     if user:
#         return user
#     raise HTTPException(
#         status_code=404,
#         detail="User not found"
#     )


# @router.get("/{contact_id}/company", summary="Gets contact's user", response_model=CompanyRead)
# async def get_contact_company(contact_id: int, db_session: AsyncSession = Depends(get_db)):
#     company =  await ContactDAO.get_company(contact_id, db_session)
#     if company:
#         return company
#     raise HTTPException(
#         status_code=404,
#         detail="Company not found"
#     )



