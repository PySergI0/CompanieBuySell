__all__ = ["User"]
from typing import Optional

from sqlalchemy import Integer, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants import UNIQ_STR_AN, GenderEnum, UserPostEnum
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[UNIQ_STR_AN]
    password: Mapped[str] = mapped_column(String(24))
    hash_password: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(30))
    middle_name: Mapped[Optional[str]] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    gender: Mapped[GenderEnum] = mapped_column(SQLEnum(GenderEnum), name="gender_enum")
    post: Mapped[UserPostEnum] = mapped_column(
        SQLEnum(UserPostEnum, name="user_post_enum"),
        default=UserPostEnum.SALES_MANAGER,
    )
    email: Mapped[UNIQ_STR_AN]
    companies: Mapped[list["Company"]] = relationship(
        "Company",
        back_populates="user",
    )
    contacts: Mapped[list["Contact"]] = relationship(
        "Contact",
        back_populates="user",
    )