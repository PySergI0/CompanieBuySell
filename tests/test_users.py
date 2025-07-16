import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models import User
from app.constants import GenderEnum, UserPostEnum


class TestUserRouters:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "username, password, first_name, last_name, gender, post, email, middle_name, expected_status",
        [
            # Стандартный кейс
            (
                "ivanov", "pass123", "Иван", "Иванов",
                GenderEnum.MALE, UserPostEnum.SALES_MANAGER,
                "ivanov@example.com", None, 201
            ),
            # Без отчества
            (
                "petrov", "pass456", "Петр", "Петров",
                GenderEnum.MALE, UserPostEnum.ROP,
                "petrov@example.com", None, 201
            ),
            # С отчеством
            (
                "sidorova", "pass789", "Мария", "Сидорова",
                GenderEnum.FEMALE, UserPostEnum.ROP,
                "sidorova@example.com", "Ивановна", 201
            ),
            # Невалидный email
            (
                "test", "pass000", "Тест", "Тестов",
                GenderEnum.MALE, UserPostEnum.SALES_MANAGER,
                "invalid-email", None, 422
            ),
        ]
    )
    async def test_create_users(self, async_client: AsyncClient, username, password, first_name,
                                last_name, gender, post, email, middle_name, expected_status):
        user_data = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "post": post,
            "email": email,
            "middle_name": middle_name
        }

        response = await async_client.post("/api/users/", json=user_data)

        assert response.status_code == expected_status
