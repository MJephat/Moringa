from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Table
# from sqlalchemy.orm import relationship
# Create an instance of SQLAlchemy
from exts import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
   
    def __repr__(self):
        return f"<User {self.userName}>"
    def save(self):
        db.session.add(self)
        db.session.commit()

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    media = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    price = db.Column(db.Text, nullable=False)
    # category = db.Column(db.String(50), nullable=False)
        
    # Define a relationship to the User model
    def __repr__(self):
        return f"<Event {self.title}>"
    def save(self):
        db.session.add(self)
        db.session.commit()

        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, host, title, media, location, time, date,price):
        self.host = host
        self.title = title
        self.media = media
        self.location = location
        self.time = time
        self.date = date

        db.session.commit()