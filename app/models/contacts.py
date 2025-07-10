__all__ = ["Contact", "ContactComment"]

from typing import Optional

from sqlalchemy import Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY, TEXT

from app.constants import CompanyPostEnum, DepartmentEnum
from app.database import Base, BaseComment
    
class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] 
    middle_name: Mapped[Optional[str]] = mapped_column(String(30), default=None)
    last_name: Mapped[Optional[str]] = mapped_column(String(30), default=None)
    email: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    phone: Mapped[list[str]] = mapped_column(ARRAY(TEXT), default=list)
    post: Mapped[Optional[CompanyPostEnum]] = mapped_column(
        SQLEnum(CompanyPostEnum, name="company_post_enum"),
        default=None,
        )
    department: Mapped[Optional[DepartmentEnum]] = mapped_column(
        SQLEnum(DepartmentEnum, name="department_enum"), 
        default=None,
    )
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship(
        "User",
        back_populates="contacts",
        cascade="save-update, merge",
    )
    company_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("companies.id"))
    company: Mapped[Optional["Company"]] = relationship(
        "Company",
        back_populates="contacts",
        cascade="save-update, merge",
    )
    comments: Mapped[list["ContactComment"]] = relationship(
        "ContactComment",
        back_populates="contact",
        cascade="all, delete-orphan",
        order_by="desc(ContactComment.created_at)",
    )
    
class ContactComment(BaseComment):
    __tablename__ = "contact_comments"
    contact_id: Mapped[int] = mapped_column(Integer, ForeignKey("contacts.id"))
    contact: Mapped["Contact"] = relationship(
        "Contact",
        back_populates="comments",
        cascade="save-update, merge",
    )