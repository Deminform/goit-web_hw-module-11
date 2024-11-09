from datetime import date, timedelta

from sqlalchemy import select, text, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.contacts.models import Contact
from src.contacts.schemas import ContactSchema, ContactUpdateSchema


async def get_contacts(limit: int, skip: int, days: int, db: AsyncSession):
    today = date.today()
    end_date = today + timedelta(days=days-1)

    day_today = today.timetuple().tm_yday
    day_end_date = end_date.timetuple().tm_yday

    if days != 0:
        if day_end_date >= day_today:
            stmt = select(Contact).where(
                func.date_part('doy', Contact.birthday).between(day_today, day_end_date)
            ).order_by(Contact.birthday).offset(skip).limit(limit)
        else:
            stmt = select(Contact).where(
                or_(
                    func.date_part('doy', Contact.birthday) >= day_today,
                    func.date_part('doy', Contact.birthday) <= day_end_date
                )
            ).order_by(Contact.birthday).offset(skip).limit(limit)
    else:
        stmt = select(Contact).offset(skip).limit(limit)

    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact_by_id(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def get_contact_by_name(contact_fullname: str, db: AsyncSession):
    stmt = select(Contact).where(Contact.fullname.ilike(f'%{contact_fullname}%'))
    contact = await db.execute(stmt)
    return contact.scalars().all()


async def get_contact_by_email(email: str, db: AsyncSession):
    stmt = select(Contact).where(Contact.email.ilike(f'%{email}%'))
    contact = await db.execute(stmt)
    return contact.scalars().all()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(contact, key, value)

    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
