from app import app
from flask import render_template, request
from bs4 import BeautifulSoup
from ebooklib import epub
from models import db, Book, Chapter
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/', methods=['GET', 'POST'])
def index():
    info = ""
    user_text = ""
    count = 0
    if request.method == 'POST':

        if 'content_text' in request.form:
            user_text = request.form.get('content_text')
            if user_text:
                soup = BeautifulSoup(user_text, 'lxml')
                if soup.head:
                    soup.head.decompose()

                clean_text = soup.get_text(separator=' ')

                words = clean_text.split()
                count = len(words)
                print(f"Количество слов: {count}")
                print("user_text", user_text)
                print("SOUP", soup)

        elif 'content_file' in request.files:
            user_file = request.files.get('content_file')
            efile = ''
            try:
                efile = epub.read_epub(user_file)

                print("TITLE:", efile.title)
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

                        chapter = Chapter(title=f'{file.get_name()}', content=str(soup.prettify()), order_number=index, book=new_book)
                        db.session.add(chapter)
                        
                    info = f'Успешно загружен файл {efile.title}'
                    logging.info(info)
                    db.session.commit()
                else:
                    info = "Book already exist"
                    logging.info(info)
            except epub.EpubException as e:
                info = "Incorrect file type"
                logging.exception(info)

    all_book = Book.query.all()
    return render_template('index.html', user_text=user_text, words_count=count, info=info, books=all_book)

@app.route('/<book>')
def book_view():
    pass
    return render_template('book.html', text=text, words_count=count, chapter=all_chapter)