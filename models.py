from app import db


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    chapters = db.relationship(
        'Chapter', backref=db.backref('book', lazy='select'), lazy='dynamic')


class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    order_number = db.Column(db.Integer)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
