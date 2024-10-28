from fastapi import FastAPI, Path, Query
from pydantic import BaseModel


app = FastAPI()


class Note(BaseModel):
    name: str
    description: str
    done: bool


@app.get('/notes')
async def read_notes(skip: int = 0, limit: int = 10, q: str | None = None):
    return {'message': f'Return all notes: skip: {skip}, limit: {limit}'}


@app.post('/notes')
async def create_note(note: Note):
    return {'name': note.name, 'description': note.description, 'status': note.done}

