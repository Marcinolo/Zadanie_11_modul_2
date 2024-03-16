from fastapi import FastAPI, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .crud import (
    get_contact,
    get_contacts,
    create_contact,
    update_contact,
    delete_contact,
    get_contacts_upcoming_birthdays
)
from .schemas import ContactBase, ContactCreate, ContactOut

# Tworzenie instancji aplikacji FastAPI
app = FastAPI()

# Tworzenie bazy danych SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./contacts.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tworzenie tabel w bazie danych
Base.metadata.create_all(bind=engine)

# Routes
@app.post("/contacts/", response_model=ContactOut)
def create_new_contact(contact: ContactCreate, db_session=SessionLocal()):
    return create_contact(db_session, contact)

@app.get("/contacts/", response_model=list[ContactOut])
def read_all_contacts(search_query: str = None, db_session=SessionLocal()):
    return get_contacts(db_session, search_query)

@app.get("/contacts/{contact_id}", response_model=ContactOut)
def read_contact(contact_id: int, db_session=SessionLocal()):
    return get_contact(db_session, contact_id)

@app.put("/contacts/{contact_id}", response_model=ContactOut)
def update_existing_contact(contact_id: int, contact: ContactCreate, db_session=SessionLocal()):
    return update_contact(db_session, contact_id, contact)

@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_contact(contact_id: int, db_session=SessionLocal()):
    return delete_contact(db_session, contact_id)

@app.get("/contacts/upcoming_birthdays", response_model=list[ContactOut])
def get_upcoming_birthdays(db_session=SessionLocal()):
    return get_contacts_upcoming_birthdays(db_session)