from flask import Blueprint, redirect, render_template, request, url_for

from models import Book, Bookmark, Chapter, db
from utils.text_helpers import words_count

books = Blueprint('books', __name__, template_folder='templates')


@books.route('/book/<int:book_id>/')
@books.route('/book/<int:book_id>/<int:chapter_id>')
def book_view(book_id, chapter_id=0):
    book = db.session.get(Book, book_id)
    if not book:
        return 'Book is not found', 404

    chapter = book.chapters.filter_by(order_number=chapter_id).first()

    if not chapter:
        return 'Chapter is not found', 404

    total_chapters = book.chapters.count()

    bookmarks = Bookmark.query.filter_by(book_id=book_id)
    if bookmarks:
        bookmarks = bookmarks.all()

    text = chapter.content
    count = words_count(text)

    return render_template(
        'books/book.html',
        text=text,
        words_count=count,
        book=book,
        chapter=chapter,
        bookmarks=bookmarks,
        total_chapters=total_chapters,
    )


@books.route('/book/<int:book_id>/<int:chapter_id>', methods=['POST'])
def set_bookmark(book_id, chapter_id):

    paragraph_id = int(request.form.get('paragraph-id', '0').replace('p-', ''))

    chapter = db.session.scalar(
        db.select(Chapter).filter_by(
            book_id=book_id, order_number=chapter_id)
    )
    if chapter.bookmark:
        chapter.bookmark.paragraph_id = paragraph_id
    else:
        chapter.bookmark = Bookmark(title=chapter.title, book_id=book_id,
                            chapter_id=chapter_id, paragraph_id=paragraph_id)

    db.session.commit()
    return {
        'status': 'success',
        'paragraph_id': paragraph_id
    }, 200


@books.route('/book/<int:book_id>/<int:chapter_id>/delete_bookmark', methods=['POST'])
def delete_bookmark(book_id, chapter_id):

    bookmark = db.session.scalar(
        db.select(Bookmark).where(
            Bookmark.book_id == book_id, Bookmark.chapter_id == chapter_id
        )
    )

    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()

    return redirect(
        request.referrer
        or url_for('books.book_view', book_id=book_id, chapter_id=chapter_id)
    )


@books.route('/book/<int:book_id>/<int:chapter_id>/edit_bookmark', methods=['POST'])
def edit_bookmark(book_id, chapter_id):
    new_title = request.form.get('new_title').strip()

    if new_title:
        bookmark = db.session.scalar(
            db.select(Bookmark).where(
                Bookmark.book_id == book_id, Bookmark.chapter_id == chapter_id
            )
        )

        if bookmark:
            bookmark.title = new_title
            db.session.commit()

    return redirect(
        request.referrer
        or url_for('books.book_view', book_id=book_id, chapter_id=chapter_id)
    )
