from sqlalchemy import MetaData, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.users.models import User


# metadata_obj = MetaData()


class Company(Base):
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    inn: Mapped[str | None]
    email: Mapped[str | None]
    phone: Mapped[str | None]

    user: Mapped[User]
    comments: Mapped[]
