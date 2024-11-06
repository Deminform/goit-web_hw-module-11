from fastapi import FastAPI, HTTPException, Depends, status, Path, Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db


router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.get('/')
async def get_contacts():
    pass

@router.get('/{contact_id}')
async def get_contact():
    pass

@router.post('/')
async def create_contact():
    pass

@router.put('/{contact_id}')
async def update_contact():
    pass

@router.delete('/{contact_id}')
async def delete_contact():
    pass
