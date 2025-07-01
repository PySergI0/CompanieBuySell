import enum
from typing import Annotated, Optional

from sqlalchemy import  Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


uniq_str_an = Annotated[str, mapped_column(unique=True)]

class GenderEnum(str, enum.Enum):
    MALE = "мужчина"
    FEMALE = "женщина"
    
class ProfessionEnum(str, enum.Enum):
        SALES_MANAGER = "менеджер по продажам"
        ROP = "Руководитель отдела продаж"


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[uniq_str_an]
    profession: Mapped[ProfessionEnum] = mapped_column(
        default=ProfessionEnum.SALES_MANAGER,
        server_default=ProfessionEnum.SALES_MANAGER,
    )
    email: Mapped[uniq_str_an]
    companies: Mapped[list["Company"]] = relationship(
        "Company",
        back_populates="user",
        cascade="save-update, merge",
    )
    
class Company(Base):
    inn: Mapped[str] = mapped_column(String(12), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    email: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]

    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship(
        "User",
        back_populates="companies",
        cascade="save-update, merge",
        lazy="joined"
    )