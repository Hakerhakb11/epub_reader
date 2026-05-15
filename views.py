from app import app
from flask import render_template, request
from bs4 import BeautifulSoup
from ebooklib import epub
from models import db, Book, Chapter
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def words_count(user_text):
    if user_text:
        soup = BeautifulSoup(user_text, 'lxml')
        if soup.head:
            soup.head.decompose()

        clean_text = soup.get_text(separator=' ')

        words = clean_text.split()
        count = len(words)
        print(f"Количество слов: {count}")
        return count
    

def add_epub_file(user_file):
    try:
        efile = epub.read_epub(user_file)

        new_book_temp = Book.query.filter_by(title=efile.title).first()
        if not new_book_temp:
            new_book = Book(title=f'{efile.title}')
            db.session.add(new_book)
            spine = efile.spine
            for index, item_spine in enumerate(spine):
                item_id = item_spine[0]
                file = efile.get_item_with_id(item_id)
                raw_content = file.get_content()
                soup = BeautifulSoup(raw_content, 'xml')

                chapter = Chapter(title=f'{file.get_name()}', content=str(
                    soup.prettify()), order_number=index, book=new_book)
                db.session.add(chapter)

            info = f'Успешно загружен файл {efile.title}'
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


@app.route('/', methods=['GET', 'POST'])
def index():
    info = ""
    user_text = ""
    count = 0
    if request.method == 'POST':

        if 'content_text' in request.form:
            user_text = request.form.get('content_text')
            count = words_count(user_text)

        elif 'content_file' in request.files:
            user_file = request.files.get('content_file')
            info = add_epub_file(user_file)

    all_book = Book.query.all()
    return render_template('index.html', user_text=user_text, words_count=count, info=info, books=all_book)


@app.route('/book/<int:book_id>/')
@app.route('/book/<int:book_id>/<int:chapter_id>')
def book_view(book_id, chapter_id=0):
    book = db.session.get(Book, book_id)
    if not book:
        return "Book is not found", 404
    
    chapter = book.chapters.filter_by(order_number=chapter_id).first()

    if not chapter:
        return "Chapter is not found", 404
    
    text = chapter.content
    count = words_count(text)

    return render_template('book.html', text=text, words_count=count, book=book)
