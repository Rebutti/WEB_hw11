from src import db
from src import models
from sqlalchemy import and_

def create_contact(first_name, last_name, birthday, email, address, cell_phone, user_id):
    contact = models.Contact(first_name=first_name, second_name=last_name, birthday=birthday, email=email, address=address, cell_phone=cell_phone, user_id=user_id)
    db.session.add(contact)
    db.session.commit()
    return contact

def get_contacts_user(user_id):
    return db.session.query(models.Contact).where(models.Contact.user_id == user_id).all()


def cont_delete(contact_id, user_id):
    # contact = get_contacts_user(contact_id, user_id)
    db.session.query(models.Contact).filter(
        and_(models.Contact.user_id == user_id, models.Contact.id == contact_id)).delete()
    db.session.commit()


def get_contact_user(contact_id, user_id):
   contact = db.session.query(models.Contact).filter(and_(models.Contact.user_id == user_id, models.Contact.id == contact_id)).one()
   return contact

def update_contact(contact_id, user_id, first_name, last_name, birthday, email, address, cell_phone):
    contact = get_contact_user(contact_id, user_id)
    if first_name != '':
        contact.first_name = first_name
    if last_name != '':
        contact.last_name = last_name
    if birthday != '':
        contact.birthday = birthday
    if email != '':
        contact.email = email
    if address != '':
        contact.address = address
    if cell_phone != '':
        contact.cell_phone = cell_phone
    
    db.session.commit()