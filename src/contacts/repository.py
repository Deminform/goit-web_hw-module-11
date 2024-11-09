from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.contacts.models import Contact
from src.contacts.schemas import ContactSchema, ContactUpdateSchema


async def get_contacts(limit:int, skip:int, db:AsyncSession):
    stmt = select(Contact).offset(skip).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact_by_id(contact_id:int, db:AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def get_contact_by_name(contact_fullname:str, db:AsyncSession):
    stmt = select(text(contact_fullname), Contact.fullname)
    contact = await db.execute(stmt)
    return contact.all()


async def create_contact(body:ContactSchema, db:AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact



async def update_contact(contact_id:int, body:ContactUpdateSchema, db:AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(contact, key, value)

    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def delete_contact(contact_id:int, db:AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
