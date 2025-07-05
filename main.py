from fastapi import FastAPI, APIRouter
import uvicorn

from app.routers.users import router as users_router

app = FastAPI()

main_router = APIRouter(prefix="/api")
main_router.include_router(users_router)

app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
