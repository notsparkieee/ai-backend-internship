from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.document import DocumentCreate, DocumentResponse
from app.models.user import User
from app.models.document import Document

app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "Backend is running"}


# -------------------- USERS --------------------

@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -------------------- DOCUMENTS --------------------

@app.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):
    # Check if owner exists
    owner = db.query(User).filter(User.id == document.owner_id).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    new_document = Document(
        title=document.title,
        owner_id=document.owner_id
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document
@app.get(
    "/users/{user_id}/documents",
    response_model=list[DocumentResponse]
)
def get_user_documents(
    user_id: int,
    db: Session = Depends(get_db)
):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Fetch documents for this user
    documents = db.query(Document).filter(Document.owner_id == user_id).all()

    return documents
