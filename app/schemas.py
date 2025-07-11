__all__ = [
    "CompanyCreate",
    "CompanyUpdate",
    "CompanyRead",
    "CompanyCommentCreate",
    "CompanyCommentUpdate",
    "CompanyCommentRead",
    "UserCreate",
    "UserResponse",
    "ContactCreate",
    "ContactUpdate",
    "ContactFullResponse",
    "ContactCommentCreate",
    "ContactCommentUpdate",
    "ContactCommentRead",
]

from datetime import datetime
from typing import List, Optional, ForwardRef
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.constants import AreaActivityEnum, CompanyPostEnum, DepartmentEnum, GenderEnum, UserPostEnum


CompanyCommentRead = ForwardRef("CompanyCommentRead")
CompanyRead = ForwardRef("CompanyRead")
ContactCommentRead = ForwardRef("ContactCommentRead")


class ContactBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    middle_name: Optional[str] = Field(None, description="Middle name (optional)")
    last_name: Optional[str] = Field(None, description="Last name (optional)")
    email: Optional[EmailStr] = Field(None, example="test@example.com")
    phone: List[str] = Field(default_factory=list, example=["+79991234567"])
    post: Optional[CompanyPostEnum] = None
    department: Optional[DepartmentEnum] = None
    user_id: Optional[int] = Field(None, gt=0, example=1)
    company_id: Optional[int] = Field(None, gt=0, example=1)

class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(
        None, min_length=2, max_length=50, example="Иван")
    middle_name: Optional[str] = Field(None, max_length=30, example="Петрович")
    last_name: Optional[str] = Field(None, max_length=30, example="Иванов")
    email: Optional[EmailStr] = Field(
        None, example="contact@example.com", description="Рабочий email")
    phone: Optional[List[str]] = Field(
        None, example=["+79991234567", "+74951234567"])
    post: Optional[CompanyPostEnum] = Field(None, example="Директор")
    department: Optional[DepartmentEnum] = Field(None, example="Отдел Продаж")
    company_id: Optional[int] = Field(None, gt=0, example=1)
    user_id: Optional[int] = Field(None, gt=0, example=1)

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Алексей",
                "last_name": "Иванов",
                "phone": ["+79998887766"],
                "post": "Менеджер по продажам",
                "department": "Отдел продаж"
            }
        }

class ContactResponse(ContactBase):
    """Response schema without relations"""
    id: int
    created_at: datetime
    updated_at: datetime
    

class ContactFullResponse(ContactResponse):
    """Response full schema with relations"""
    user: Optional["UserResponse"] = None
    company: Optional["CompanyRead"] = None
    comments: List["ContactCommentRead"] = []


class ContactCommentCreate(BaseModel):
    text: str
    contact_id: int


class ContactCommentUpdate(BaseModel):
    text: Optional[str] = None


class ContactCommentRead(BaseModel):
    id: int
    text: str
    # contact_id: int
    # contact: Optional["ContactResponse"] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    gender: GenderEnum
    post: UserPostEnum = UserPostEnum.SALES_MANAGER
    email: EmailStr


class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=30, example="Ibra")
    first_name: Optional[str] = Field(None, min_length=2, max_length=30, example="Иван")
    middle_name: Optional[str] = Field(None, min_length=2, max_length=30, example="Олегович")
    last_name: Optional[str] = Field(None, min_length=2, max_length=30, example="Ibra")
    gender: Optional[GenderEnum] = Field(None, example="Мужчина")
    post: Optional[UserPostEnum] = Field(None, example="Менеджер по продажам")
    email: Optional[EmailStr] = Field(None, example="contact@example.com")
    password: Optional[str] = Field(None, example="Password")


class UserResponse(UserBase):
    """Response schema without relations"""
    id: int


class UserFullResponse(UserResponse):
    """Response full schema with relations"""
    contacts: List["ContactResponse"] = []
    # companies: 


class CompanyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    inn: str = Field(..., min_length=8, max_length=12, example="12345678")
    name: str = Field(..., max_length=128, example="ООО Рога и Копыта")
    email: List[EmailStr] = Field(
        default_factory=list, example=["test@example.com"])
    phone: List[str] = Field(default_factory=list, example=["+79991234567"])
    revenue: Optional[int] = None
    area_activity: Optional[List[AreaActivityEnum]] = None
    user_id: Optional[int] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    inn: Optional[str] = Field(
        None,
        min_length=8,
        max_length=12,
        pattern="^[0-9]*$",
        example="123456789012"
    )
    name: Optional[str] = Field(
        None, max_length=128, example="ООО Рога и Копыта")
    email: Optional[List[EmailStr]] = Field(None, example=["info@company.com"])
    phone: Optional[List[str]] = Field(None, example=["+79991234567"])
    revenue: Optional[int] = None
    area_activity: Optional[List[AreaActivityEnum]] = None
    user_id: Optional[int] = Field(None, example=1)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Новое название компании",
                "phone": ["+79998887766"],
                "area_activity": ["IT"]
            }
        }


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

class CompanyFullRead(CompanyRead):
    user: Optional["UserResponse"] = None
    comments: List["CompanyCommentRead"] = Field(default_factory=list)


class CompanyCommentCreate(BaseModel):
    text: str
    contact_id: int


class CompanyCommentUpdate(BaseModel):
    text: Optional[str] = None


class CompanyCommentRead(BaseModel):
    id: int
    text: str
    company_id: int
    company: Optional["CompanyRead"] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


CompanyCommentRead.model_rebuild()
CompanyRead.model_rebuild()
ContactCommentRead.model_rebuild()
