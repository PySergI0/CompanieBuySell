from fastapi import FastAPI, APIRouter, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from app.routers import (companies_router, contacts_router, users_router)

app = FastAPI()

main_router = APIRouter(prefix="/api")
main_router.include_router(users_router)
main_router.include_router(contacts_router)
main_router.include_router(companies_router)

app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
