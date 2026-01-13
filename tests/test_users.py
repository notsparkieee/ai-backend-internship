from tests.conftest import client


def test_create_user():
    response = client.post(
        "/users",
        json={"name": "Test User", "email": "testuser@gmail.com"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@gmail.com"


def test_duplicate_user():
    response = client.post(
        "/users",
        json={"name": "Test User", "email": "testuser@gmail.com"}
    )
    assert response.status_code == 400
