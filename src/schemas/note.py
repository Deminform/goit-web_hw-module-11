from pydantic import BaseModel


class NoteModel(BaseModel):
    name: str
    description: str
    done: bool
