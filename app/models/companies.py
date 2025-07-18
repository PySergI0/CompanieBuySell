__all__ = ["Company", "CompanyComment"]

from typing import Optional

from sqlalchemy import Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY, TEXT

from app.constants import AreaActivityEnum
from app.database import Base, BaseComment


class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inn: Mapped[str] = mapped_column(String(12), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    email: Mapped[list[str]] = mapped_column(ARRAY(TEXT), default=list)
    phone: Mapped[list[str]] = mapped_column(ARRAY(TEXT), default=list)
    revenue: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    area_activity: Mapped[Optional[list[AreaActivityEnum]]] = mapped_column(
        ARRAY(SQLEnum(AreaActivityEnum, name="area_activity_enum")),
        default=None,
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="companies",
    )
    contacts: Mapped[list["Contact"]] = relationship(
        "Contact",
        back_populates="company",
    )
    comments: Mapped[list["CompanyComment"]] = relationship(
        "CompanyComment",
        back_populates="company",
        order_by="desc(CompanyComment.created_at)",
    )


class CompanyComment(BaseComment):
    __tablename__ = "company_comments"
    company_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey(
            "companies.id",
            ondelete="CASCADE",
        ),
    )
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="comments",
    )
