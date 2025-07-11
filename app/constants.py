__ALL__ = [
    "UNIQ_STR_AN",
    "GenderEnum",
    "UserPostEnum",
    "CompanyPostEnum",
    "DepartmentEnum",
    "AreaActivityEnum",
]

import enum
from typing import Annotated

from sqlalchemy.orm import mapped_column


UNIQ_STR_AN = Annotated[str, mapped_column(unique=True)]


class GenderEnum(str, enum.Enum):
    MALE = "Мужчина"
    FEMALE = "Женщина"


class UserPostEnum(str, enum.Enum):
    SALES_MANAGER = "Менеджер по продажам"
    ROP = "Руководитель отдела продаж"


class CompanyPostEnum(str, enum.Enum):
    PURCHASE_MANAGER = "Менеджер по закупкам"
    DIRECTOR = "Директор"
    HEAD_DEPARTMENT = "Начальник отдела"


class DepartmentEnum(str, enum.Enum):
    SALES = "Отдел продаж"
    PURCHASE = "Отдел закупок"
    ACCOUNTING = "Бухгалтерия"


class AreaActivityEnum(str, enum.Enum):
    pass
