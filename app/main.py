from fastapi import FastAPI, status, HTTPException
from app.schemas.user import UserCreate, UserResponse

app = FastAPI()

# Temporary in-memory storage (will be replaced by DB later)
fake_users_db = []


@app.get("/")
def health_check():
    return {"status": "Backend is running"}


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):

    # Check for duplicate email
    for existing_user in fake_users_db:
        if existing_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

    fake_users_db.append(user)
    return user
