from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    chapters = db.relationship(
        'Chapter',
        backref=db.backref('book', lazy='select'),
        lazy='dynamic',
        cascade='all, delete-orphan',
    )
    bookmarks = db.relationship('Bookmark', cascade='all, delete-orphan')


class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    order_number = db.Column(db.Integer)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    bookmark = db.relationship(
        'Bookmark', backref='chapter', uselist=False, cascade="all, delete-orphan")


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    paragraph_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey(
        'chapters.id'), nullable=False)


class Config(db.Model):
    __tablename__ = 'configs'
    id = db.Column(db.Integer, primary_key=True)
    config_json = db.Column(db.JSON, nullable=False)
