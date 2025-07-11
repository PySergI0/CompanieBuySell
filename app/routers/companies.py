from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Company
from app.schemas import CompanyFullResponse, CompanyResponse, CompanyCreate, CompanyUpdate
from app.database.dao import CompanyDAO

router = APIRouter(prefix="/companies", tags=["companies/"])

@router.get("/", summary="Gets all companies", response_model=list[CompanyResponse])
async def get_companies(db_session: AsyncSession = Depends(get_db)):
    return await CompanyDAO.get_all(db_session)

@router.get("/{company_id}", summary="Gets detail company's info", response_model=CompanyFullResponse)
async def get_company_detail(company_id: int, db_session: AsyncSession = Depends(get_db)):
    company = await CompanyDAO.get_details(company_id, db_session)
    if company:
        return company
    raise HTTPException(
        status_code=404,
        detail="Company with ID {company_id} not found"
    )

@router.post(
        "/",
        summary="Create new company",
        status_code=status.HTTP_201_CREATED,
        response_model=CompanyResponse,
    )
async def create_companies(contact_data: CompanyCreate, db: AsyncSession = Depends(get_db)):
    result = await CompanyDAO.create_new_record(contact_data, db)
    if isinstance(result, Company):
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
    
@router.delete("/{company_id}", summary="Delete company", status_code=status.HTTP_200_OK)
async def delete_contact(company_id: int, db: AsyncSession = Depends(get_db)):
    result = await CompanyDAO.delete_record(company_id, db)
    if result:
        return {"status": "success", "deleted_id": company_id}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Company with id {company_id} not found",
    ) 


@router.patch(
        "/{contact_id}", 
        summary="Update contact", 
        status_code=status.HTTP_200_OK, 
        response_model=CompanyResponse
    )
async def update_contact(contact_id: int, data: CompanyUpdate, db: AsyncSession = Depends(get_db)):
    result = await CompanyDAO.update_record(contact_id, data, db)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error"
    )