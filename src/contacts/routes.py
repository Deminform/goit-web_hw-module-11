from fastapi import HTTPException, Depends, status, Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from src.contacts import repository as repo_contacts
from src.contacts.schemas import ContactSchema, ContactResponseSchema, ContactUpdateSchema

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get('/', response_model=list[ContactResponseSchema])
async def get_contacts(
        limit: int = Query(10, ge=10, le=100),
        offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_db)):

    contacts = await repo_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get('/search', response_model=ContactResponseSchema)
async def get_contact(contact_id: int = None, fullname: str = None, db: AsyncSession = Depends(get_db)):
    contact = None
    if id:
        contact = await repo_contacts.get_contact_by_id(contact_id, db)

    elif fullname:
        contact = await repo_contacts.get_contact_by_name(fullname, db)

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact



# @router.get('/{contact_id}', response_model=ContactResponseSchema)
# async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
#     contact = await repo_contacts.get_contact_by_id(contact_id, db)
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
#     return contact


@router.post('/', response_model=ContactResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await repo_contacts.create_contact(body, db)
    return contact


@router.put('/{contact_id}')
async def update_contact(body: ContactUpdateSchema, contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await repo_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await repo_contacts.delete_contact(contact_id, db)
    return contact
