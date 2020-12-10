from datetime import date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=True)


class Contact(db.Model):
    __tablename__ = 'contacts'
    uid = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String(50), nullable=True)
    sender_phone = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    date = db.Column(db.String(255), default=lambda: date.today())
