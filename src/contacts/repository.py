from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.contacts.models import Contact
from src.contacts.schemas import ContactSchema


async def get_contacts(limit:int, skip:int, db:AsyncSession):
    stmt = select(Contact).offset(skip).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id:int, db:AsyncSession):
    stmt = select(Contact).filter_by(contact_id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body:ContactSchema, db:AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact



async def update_contact():
    pass


async def delete_contact():
    pass