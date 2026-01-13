from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tempfile
import os

from app.database import get_db
from app.models.user import User
from app.models.document import Document
from app.schemas.user import UserCreate, UserResponse
from app.schemas.document import DocumentCreate, DocumentResponse

# ✅ CORRECT imports (FIXED)
from app.vector_store import (
    index_document_chunks,
    search_similar_chunks,
)

from app.agents.graph import qa_agent

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

# -------------------------
# USERS
# -------------------------

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# -------------------------
# DOCUMENT METADATA
# -------------------------

@app.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.id == document.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="User not found")

    doc = Document(
        title=document.title,
        owner_id=document.owner_id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@app.get("/users/{user_id}/documents", response_model=list[DocumentResponse])
def get_user_documents(user_id: int, db: Session = Depends(get_db)):
    return db.query(Document).filter(Document.owner_id == user_id).all()


# -------------------------
# OCR HELPERS
# -------------------------

def extract_text_from_image(path: str) -> str:
    image = Image.open(path)
    return pytesseract.image_to_string(image)


def extract_text_from_pdf(path: str) -> str:
    pages = convert_from_path(path)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page) + "\n"
    return text


# -------------------------
# OCR UPLOAD
# -------------------------

@app.post("/documents/upload", status_code=201)
def upload_document(
    owner_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    owner = db.query(User).filter(User.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="User not found")

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.file.read())
        temp_path = tmp.name

    try:
        if file.content_type.startswith("image/"):
            extracted_text = extract_text_from_image(temp_path)
        elif file.content_type == "application/pdf":
            extracted_text = extract_text_from_pdf(temp_path)
        else:
            raise HTTPException(status_code=415, detail="Unsupported file type")
    finally:
        os.remove(temp_path)

    document = Document(
        title=file.filename,
        content=extracted_text,
        owner_id=owner_id,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # ✅ INDEX CHUNKS INTO FAISS
    index_document_chunks(document.id, document.content, document.owner_id)

    return {
        "document_id": document.id,
        "extracted_text": extracted_text,
    }


# -------------------------
# SEMANTIC SEARCH (DEBUG)
# -------------------------

@app.post("/search")
def semantic_search(query: str, owner_id: int, top_k: int = 5):
    return search_similar_chunks(query, owner_id, top_k)


# -------------------------
# AI ASK (PHASE 4)
# -------------------------

class AskRequest(BaseModel):
    question: str
    owner_id: int


@app.post("/ai/ask")
def ask_ai(req: AskRequest):
    result = qa_agent.invoke({"question": req.question, "owner_id": req.owner_id})
    return {"answer": result["answer"]}


@app.get("/debug/index_size")
def get_index_size():
    from app.vector_store import index, chunk_metadata
    return {
        "index_size": index.ntotal,
        "metadata_count": len(chunk_metadata),
        "owners": list(set([m["owner_id"] for m in chunk_metadata])) if chunk_metadata else []
    }


@app.get("/debug/test_search")
def test_search(owner_id: int, query: str = "test"):
    from app.vector_store import search_similar_chunks
    results = search_similar_chunks(query, owner_id, top_k=5)
    return {
        "query": query,
        "owner_id": owner_id,
        "results_count": len(results),
        "results": results[:2] if results else []
    }
