import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db
from tests.test_database import TestingSessionLocal, create_test_db, drop_test_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    create_test_db()
    yield
    drop_test_db()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
