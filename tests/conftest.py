import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.database import Base, get_db

# Настройка тестовой SQLite базы данных в памяти (опционально, если хотите реальную БД для некоторых тестов)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Фикстура для создания тестовой БД (если нужно)
@pytest.fixture(scope="function")
def db_session():
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Фикстура для мока базы данных
@pytest.fixture(scope="function")
def mock_db():
    with patch('database.get_db') as mock:
        mock_db = MagicMock()
        mock.return_value = mock_db
        yield mock_db

# Фикстура для тестового клиента
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

# Фикстура для авторизованного клиента (если нужно)
@pytest.fixture(scope="function")
def authorized_client(test_client, mock_db):
    # Здесь можно добавить логику аутентификации
    # Например, мокировать токен или JWT
    test_client.headers.update({"Authorization": "Bearer mocktoken"})
    return test_client