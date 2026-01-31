from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import List
from database import get_db, init_db
from models import Contact


app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContactResponse(BaseModel):
    id:int
    name: str
    email: EmailStr
    message: str

    class Config:
        from_attributes = True

@app.get("/health")
def health_check():
    return {"status": "ok"}



@app.post("/contacts",response_model = ContactResponse, status_code = 201)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    try:
        db_contact = Contact(
            name = contact.name.strip(),
            email = contact.email.strip(),
            message = contact.message.strip()
        )
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)

        return ContactResponse(
            id = db_contact.id,
            name = db_contact.name,
            email = db_contact.email,
            message = db_contact.message
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail = str(e))