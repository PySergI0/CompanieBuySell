import enum
from sqlalchemy import MetaData, String
from src.database import Base, uniq_str_an
from sqlalchemy.orm import Mapped, mapped_column, relationship

class GenderEnum(str, enum.Enum):
    MALE = "мужчина"
    FEMALE = "женщина"
    
class ProfessionEnum(str, enum.Enum):
        SALES_MANAGER = "менеджер по продажам"


class User(Base):
    username: Mapped[uniq_str_an]
    profession: Mapped[str] = mapped_column()
    email: Mapped[uniq_str_an]
    