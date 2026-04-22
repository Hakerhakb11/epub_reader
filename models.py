from app import db

class Book(db.Model):
    id = id.Column(db.Integer, primary_key=True)
    