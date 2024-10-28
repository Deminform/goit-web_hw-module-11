from fastapi import Depends, FastAPI, Path, Query, HTTPException
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.entity.models import Note
from src.schemas.note import NoteModel

app = FastAPI()


@app.get('/api/healthchecker')
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute('SELECT 1').fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail='Database config Error')
        return {'message': 'Welcome to FastAPI'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Database connection Error')


@app.post('/notes')
async def create_note(note: NoteModel, db: Session = Depends(get_db())):
    new_note = Note(name=note.name, description=note.description, done=note.done)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note
