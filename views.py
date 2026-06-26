from flask import render_template, request

from app import app
from models import Book
from utils.text_helpers import add_epub_file, words_count


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
        "index/index.html", user_text=user_text, words_count=count, info=info, books=all_book
    )
