from fastapi import Depends, FastAPI, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from src.database.db import get_db
from src.entity.models import Note
from src.schemas.note import NoteModel, NoteResponseModel

app = FastAPI()


@app.get('/api/healthchecker', tags=['Healthchecker'])
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute('SELECT 1').fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail='Database config Error')
        return {'message': 'Welcome to FastAPI'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Database connection Error')


# @app.get('/notes', tags=['Notes'])
# async def read_notes(skip: int = 0, limit: int = Query(default=10, le=100, ge=10), db: Session = Depends(get_db)):
#     notes = db.query(Note).offset(skip).limit(limit).all()
#     return notes


@app.get('/notes)', tags=['Notes'])
async def read_notes(
        skip: int = 0,
        limit: int = Query(default=10, le=100, ge=10),
        db: Session = Depends(get_db)) -> list[NoteResponseModel]:
    notes = db.query(Note).offset(skip).limit(limit).all()
    return notes


@app.post('/notes', tags=['Notes'])
async def create_note(note: NoteModel, db: Session = Depends(get_db)):
    new_note = Note(name=note.name, description=note.description, done=note.done)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@app.get('/notes/{note_id}', tags=['Notes'], response_model=NoteResponseModel)
async def read_note(note_id: int = Path(description='The ID of the note to get', gt=0, le=100),
                    db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return note





