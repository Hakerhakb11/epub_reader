from flask import flash, redirect, render_template, request, url_for

from app import app
from models import Book, db
from utils.text_helpers import add_epub_file, words_count


@app.route("/", methods=["GET", "POST"])
def index():
    user_text = ""
    count = 0
    if request.method == "POST":
        if "content_text" in request.form:
            user_text = request.form.get("content_text")
            count = words_count(user_text)

        elif "content_file" in request.files:
            user_file = request.files.get("content_file")
            info = add_epub_file(user_file)
            flash(info)

    all_book = Book.query.all()
    return render_template(
        "index/index.html", user_text=user_text, words_count=count, books=all_book
    )


@app.route("/<int:book_id>/delete_book", methods=["POST"])
def delete_book(book_id):

    book = db.session.scalar(db.select(Book).where(
        Book.id == book_id
    ))
    if book:
        db.session.delete(book)
        db.session.commit()
        info = 'The Book has been sucessfully deleted'
        flash(info)
    return redirect(url_for('index'))
