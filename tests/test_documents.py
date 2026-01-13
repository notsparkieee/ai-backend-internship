from tests.conftest import client
import uuid


def create_test_user():
    # Generate a unique email every time
    unique_email = f"docowner_{uuid.uuid4()}@gmail.com"

    response = client.post(
        "/users",
        json={
            "name": "Doc Owner",
            "email": unique_email
        }
    )

    # Ensure user creation succeeded
    assert response.status_code == 201

    return response.json()["id"]


def test_create_document():
    user_id = create_test_user()

    response = client.post(
        "/documents",
        json={
            "title": "Test Doc",
            "owner_id": user_id
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test Doc"
    assert response.json()["owner_id"] == user_id


def test_get_user_documents():
    user_id = create_test_user()

    # Create a document for this user
    client.post(
        "/documents",
        json={
            "title": "Another Doc",
            "owner_id": user_id
        }
    )

    response = client.get(f"/users/{user_id}/documents")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
