from pydantic import BaseModel


class DocumentCreate(BaseModel):
    title: str
    owner_id: int


class DocumentResponse(BaseModel):
    id: int
    title: str
    owner_id: int
