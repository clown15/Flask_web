from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64),nullable=False)
    name = db.Column(db.String(8),nullable=False)