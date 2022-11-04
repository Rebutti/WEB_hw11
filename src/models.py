from src import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    token_cookie = db.Column(db.String(255), nullable=True, default=None)
    pictures = relationship('Picture', back_populates='user')
    contacts = relationship('Contact', back_populates='user')

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email})"

class Picture(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(350), unique=True,nullable=False)
    description = db.Column(db.String(120), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', cascade='all, delete', back_populates='pictures')
    def __repr__(self):
        return f"Picture({self.id}, {self.path}, {self.size})"


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    cell_phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', cascade='all, delete', back_populates='contacts')
    def __repr__(self):
        return f"Picture({self.id}, {self.first_name}, {self.second_name})"
    