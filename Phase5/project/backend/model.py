from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Table
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