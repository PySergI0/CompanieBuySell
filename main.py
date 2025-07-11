from fastapi import FastAPI, APIRouter, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from app.routers import users
from app.routers import contacts

app = FastAPI()

main_router = APIRouter(prefix="/api")
main_router.include_router(users.router)
main_router.include_router(contacts.router)

app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
