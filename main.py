from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from src.contacts import routes

app = FastAPI()
app.include_router(routes.router, prefix="/api")


@app.get('/')
def index():
    return {"message": "Contacts Application"}


@app.get('/api/healthchecker')
async def healthcheck(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Database is healthy"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

