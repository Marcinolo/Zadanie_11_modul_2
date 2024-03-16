from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
from .models import Contact
from .schemas import ContactCreate

def get_contact(db_session: Session, contact_id: int):
    return db_session.query(Contact).filter(Contact.id == contact_id).first()

def get_contacts(db_session: Session, search_query: str = None):
    if search_query:
        return db_session.query(Contact).filter(or_(
            Contact.first_name.ilike(f"%{search_query}%"),
            Contact.last_name.ilike(f"%{search_query}%"),
            Contact.email.ilike(f"%{search_query}%")
        )).all()
    else:
        return db_session.query(Contact).all()

def create_contact(db_session: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db_session.add(db_contact)
    db_session.commit()
    db_session.refresh(db_contact)
    return db_contact

def update_contact(db_session: Session, contact_id: int, contact: ContactCreate):
    db_contact = get_contact(db_session, contact_id)
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db_session.commit()
    db_session.refresh(db_contact)
    return db_contact

def delete_contact(db_session: Session, contact_id: int):
    db_contact = get_contact(db_session, contact_id)
    db_session.delete(db_contact)
    db_session.commit()
    return {"message": "Contact deleted successfully"}

def get_contacts_upcoming_birthdays(db_session: Session):
    today = datetime.today()
    end_date = today + timedelta(days=7)
    return db_session.query(Contact).filter(
        (Contact.birth_date >= today) & (Contact.birth_date <= end_date)
    ).all()