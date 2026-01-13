from pydantic import BaseModel
from typing import Optional


class DocumentCreate(BaseModel):
    title: str
    owner_id: int


class DocumentResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    owner_id: int

    class Config:
        from_attributes = True
