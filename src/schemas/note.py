from pydantic import BaseModel
from pydantic import Field


class NoteModel(BaseModel):
    name: str
    description: str
    done: bool


class NoteResponseModel(NoteModel):
    id: int = Field(default=1, ge=1)
