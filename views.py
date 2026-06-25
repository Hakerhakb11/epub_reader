from app import app
from flask import render_template, request, redirect, url_for
from bs4 import BeautifulSoup
from ebooklib import epub
from models import db, Book, Chapter, Bookmark
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def words_count(user_text):
    if user_text:
        soup = BeautifulSoup(user_text, "lxml")
        if soup.head:
            soup.head.decompose()

        clean_text = soup.get_text(separator=" ")

        words = clean_text.split()
        count = len(words)
        print(f"Количество слов: {count}")
        return count


def add_epub_file(user_file):
    try:
        efile = epub.read_epub(user_file)

        new_book = Book.query.filter_by(title=efile.title).first()
        if not new_book:
            new_book = Book(title=f"{efile.title}")
            db.session.add(new_book)
            spine = efile.spine
            for index, item_spine in enumerate(spine):
                item_id = item_spine[0]
                file = efile.get_item_with_id(item_id)
                raw_content = file.get_content()
                soup = BeautifulSoup(raw_content, "xml")
                title = file.get_name().replace("Text/", '').replace(".xhtml", '')

                chapter = Chapter(
                    title=title,
                    content=str(soup.prettify()),
                    order_number=index,
                    book=new_book,
                )
                db.session.add(chapter)

            info = f"Succesfully imported file: {efile.title}"
            logging.info(info)
            db.session.commit()
            return info
        else:
            info = "Book already exist"
            logging.info(info)
            return info
    except epub.EpubException:
        info = "Incorrect file type need '.epub'"
        logging.error(info)
        return info
    except KeyError:
        info = "Incorrect file type need '.epub'"
        logging.error(info)
        return info


@app.route("/", methods=["GET", "POST"])
def index():
    info = ""
    user_text = ""
    count = 0
    if request.method == "POST":
        if "content_text" in request.form:
            user_text = request.form.get("content_text")
            count = words_count(user_text)

        elif "content_file" in request.files:
            user_file = request.files.get("content_file")
            info = add_epub_file(user_file)

    all_book = Book.query.all()
    return render_template(
        "index.html", user_text=user_text, words_count=count, info=info, books=all_book
    )


@app.route("/book/<int:book_id>/")
@app.route("/book/<int:book_id>/<int:chapter_id>")
def book_view(book_id, chapter_id=0):
    book = db.session.get(Book, book_id)
    if not book:
        return "Book is not found", 404

    chapter = book.chapters.filter_by(order_number=chapter_id).first()

    if not chapter:
        return "Chapter is not found", 404

    total_chapters = book.chapters.count()

    bookmarks = Bookmark.query.filter_by(book_id=book_id)
    if bookmarks:
        bookmarks = bookmarks.all()

    text = chapter.content
    count = words_count(text)

    return render_template(
        "book.html",
        text=text,
        words_count=count,
        book=book,
        chapter=chapter,
        bookmarks=bookmarks,
        total_chapters=total_chapters,
    )


@app.route("/book/<int:book_id>/<int:chapter_id>", methods=["GET", "POST"])
def set_bookmark(book_id, chapter_id):

    new_mark = Bookmark.query.filter_by(
        book_id=book_id, chapter_id=chapter_id).first()
    if not new_mark:
        title = db.session.scalar(db.select(Chapter).filter_by(
            book_id=book_id, order_number=chapter_id)).title
        print(title, "title")
        new_mark = Bookmark(
            title=title, book_id=book_id, chapter_id=chapter_id
        )
        db.session.add(new_mark)
        db.session.commit()
    else:
        info = "Bookmark already exist"
        logging.info(info)
        return info

    return redirect(url_for("book_view", book_id=book_id, chapter_id=chapter_id))


@app.route("/book/<int:book_id>/<int:chapter_id>/delete_bookmark", methods=["POST"])
def delete_bookmark(book_id, chapter_id):

    bookmark = db.session.scalar(db.select(Bookmark).where(
        Bookmark.book_id == book_id, Bookmark.chapter_id == chapter_id))
    
    if (bookmark):
        db.session.delete(bookmark)
        db.session.commit()
    
    return redirect(url_for('book_view', book_id=book_id, chapter_id=chapter_id))
