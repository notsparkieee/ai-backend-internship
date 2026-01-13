from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tempfile
import os
from app.vector_store import add_document, search_documents

from app.database import get_db
from app.models.user import User
from app.models.document import Document
from app.schemas.user import UserCreate, UserResponse
from app.schemas.document import DocumentCreate, DocumentResponse
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()


# -------------------------
# USERS
# -------------------------

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -------------------------
# DOCUMENTS (METADATA)
# -------------------------

@app.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.id == document.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="User not found")

    new_document = Document(
        title=document.title,
        owner_id=document.owner_id
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document


@app.get("/users/{user_id}/documents", response_model=list[DocumentResponse])
def get_user_documents(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(Document).filter(Document.owner_id == user_id).all()


# -------------------------
# OCR HELPERS
# -------------------------

def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def extract_text_from_pdf(pdf_path: str) -> str:
    pages = convert_from_path(pdf_path)
    full_text = ""

    for page in pages:
        text = pytesseract.image_to_string(page)
        full_text += text + "\n"

    return full_text


# -------------------------
# OCR UPLOAD ENDPOINT
# -------------------------

@app.post("/documents/upload", status_code=201)
def upload_document(
    owner_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    owner = db.query(User).filter(User.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="User not found")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.file.read())
        temp_path = temp_file.name

    try:
        if file.content_type.startswith("image/"):
            extracted_text = extract_text_from_image(temp_path)

        elif file.content_type == "application/pdf":
            extracted_text = extract_text_from_pdf(temp_path)

        else:
            raise HTTPException(
                status_code=415,
                detail="Unsupported file type"
            )

    finally:
        os.remove(temp_path)

    document = Document(
        title=file.filename,
        content=extracted_text,
        owner_id=owner_id
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "document_id": document.id,
        "extracted_text": extracted_text
    }
@app.post("/documents/index")
def index_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if not document.content:
        raise HTTPException(status_code=400, detail="Document has no content")

    add_document(document.id, document.content)

    return {"message": "Document indexed successfully"}
@app.post("/search")
def semantic_search(
    query: str,
    top_k: int = 5,
    db: Session = Depends(get_db)
):
    doc_ids = search_documents(query, top_k)

    documents = db.query(Document).filter(
        Document.id.in_(doc_ids)
    ).all()

    return documents