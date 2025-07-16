__all__ = [
    "CompanyCreate",
    "CompanyUpdate",
    "CompanyResponse",
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
CompanyResponse = ForwardRef("CompanyRead")
ContactCommentRead = ForwardRef("ContactCommentRead")


class ContactBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str = Field(
        ...,
        min_length=3,
        max_length=24,
        description="Имя",
        json_schema_extra={"example": "Иван"},
    )
    middle_name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=24,
        description="Отчество",
        json_schema_extra={"example": "Сергеевич"},
    )
    last_name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=24,
        description="Фамилия",
        json_schema_extra={"example": "Сергеев"},
    )
    email: Optional[EmailStr] = Field(
        None,
        min_length=3,
        max_length=24,
        description="Электронная почта",
        json_schema_extra={"example": "test@example.com"},
    )
    phone: list[str] = Field(
        default_factory=list,
        max_length=7,
        description="Номер телефона",
        json_schema_extra={
            "example": ["+79991234567", "89007564312"],
            "maxItems": 7,
        },
    )
    post: Optional[CompanyPostEnum] = Field(
        None,
        description="Должность",
        json_schema_extra={
            "enum": [e.value for e in CompanyPostEnum],
            "example": CompanyPostEnum.DIRECTOR.value,
        },
    )
    department: Optional[DepartmentEnum] = Field(
        None,
        description="Подразделение (отдел)",
        json_schema_extra={
            "enum": [d.value for d in DepartmentEnum],
            "example": DepartmentEnum.PURCHASE.value,
        },
    )
    user_id: Optional[int] = Field(
        None,
        gt=0,
        description="ID ответственного пользователя",
        json_schema_extra={"example": 1},
    )
    company_id: Optional[int] = Field(
        None,
        gt=0,
        description="ID компании контакта",
        json_schema_extra={"example": 1},
    )


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    first_name: Optional[str] = Field(
        None,
        **ContactBase.model_fields["first_name"]._attributes_set)
    middle_name: Optional[str] = Field(
        **ContactBase.model_fields["middle_name"]._attributes_set)
    last_name: Optional[str] = Field(
        **ContactBase.model_fields["last_name"]._attributes_set)
    email: Optional[EmailStr] = Field(
        **ContactBase.model_fields["email"]._attributes_set)
    phone: Optional[List[str]] = Field(
        **ContactBase.model_fields["phone"]._attributes_set)
    post: Optional[CompanyPostEnum] = Field(
        **ContactBase.model_fields["post"]._attributes_set)
    department: Optional[DepartmentEnum] = Field(
        **ContactBase.model_fields["department"]._attributes_set)
    company_id: Optional[int] = Field(
        **ContactBase.model_fields["company_id"]._attributes_set)
    user_id: Optional[int] = Field(
        **ContactBase.model_fields["user_id"]._attributes_set)


class ContactResponse(ContactBase):
    """Response schema without relations"""
    id: int = Field(..., gt=0)
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обнволения")


class ContactFullResponse(ContactResponse):
    """Response full schema with relations"""
    user: Optional["UserResponse"] = Field(
        None, description="Ответственный пользователь")
    company: Optional["CompanyResponse"] = Field(
        None, description="Компания контакта")
    comments: List["ContactCommentRead"] = Field(
        default_factory=list, description="Комментарии к контакту")


class BaseContactComment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    text: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description="Текст комментария"
    )


class ContactCommentCreate(BaseContactComment):
    contact_id: int = Field(..., gt=0, description="ID контакта")


class ContactCommentUpdate(BaseContactComment):
    id: int = Field(..., gt=0, description="ID комментария")


class ContactCommentRead(BaseContactComment):
    id: int = Field(..., gt=0, description="ID комментария")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обнволения")


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(..., )
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    gender: GenderEnum
    post: UserPostEnum = UserPostEnum.SALES_MANAGER
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None, min_length=2, max_length=30, example="Ibra")
    first_name: Optional[str] = Field(
        None, min_length=2, max_length=30, example="Иван")
    middle_name: Optional[str] = Field(
        None, min_length=2, max_length=30, example="Олегович")
    last_name: Optional[str] = Field(
        None, min_length=2, max_length=30, example="Ibra")
    gender: Optional[GenderEnum] = Field(None, example="Мужчина")
    post: Optional[UserPostEnum] = Field(None, example="Менеджер по продажам")
    email: Optional[EmailStr] = Field(None, example="contact@example.com")
    password: Optional[str] = Field(None, example="Password")


class UserResponse(UserBase):
    """Response schema without relations"""
    id: int


class UserFullResponse(UserResponse):
    """Response full schema with relations"""
    contacts: List["ContactResponse"] = Field(default_factory=list)
    companies: List["CompanyResponse"] = Field(default_factory=list)


class CompanyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    inn: str = Field(..., min_length=8, max_length=12, example="12345678")
    name: str = Field(..., max_length=128, example="ООО Рога и Копыта")
    email: List[EmailStr] = Field(
        default_factory=list, example=["test@example.com"])
    phone: List[str] = Field(default_factory=list, example=["+79991234567"])
    revenue: Optional[int] = Field(None, example=456854)
    area_activity: Optional[List[AreaActivityEnum]] = Field(
        default_factory=list, example="")
    user_id: Optional[int] = Field(None, gt=0, example=1)


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
    revenue: Optional[int] = Field(
        None, example=["+79991234567", "+79899006751"])
    area_activity: Optional[List[AreaActivityEnum]] = Field(None, example="")
    user_id: Optional[int] = Field(None, gt=1, example=1)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Новое название компании",
                "email": ["example@mail.ru"],
                "phone": ["+79998887766"],
            }
        }


class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime


class CompanyFullResponse(CompanyResponse):
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
    company: Optional["CompanyResponse"] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


CompanyCommentRead.model_rebuild()
CompanyResponse.model_rebuild()
ContactCommentRead.model_rebuild()
