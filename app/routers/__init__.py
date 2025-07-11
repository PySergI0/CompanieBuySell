from .companies import router as companies_router
from .contacts import router as contacts_router
from .users import router as users_router

__all__ = [
    "companies_router",
    "contacts_router",
    "users_router",
]