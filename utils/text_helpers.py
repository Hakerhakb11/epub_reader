import logging

from bs4 import BeautifulSoup
from ebooklib import epub

from models import Book, Chapter, db

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
        print(f'Количество слов: {count}')
        return count


def add_epub_file(user_file):
    try:
        efile = epub.read_epub(user_file)

        new_book = Book.query.filter_by(title=efile.title).first()
        if not new_book:
            new_book = Book(title=f'{efile.title}')
            db.session.add(new_book)
            spine = efile.spine
            for index, item_spine in enumerate(spine):
                item_id = item_spine[0]
                file = efile.get_item_with_id(item_id)
                title = file.get_name().rsplit(
                    '/', 1)[-1].replace('.xhtml', '')

                soup = clear_chapters(file)

                chapter = Chapter(
                    title=title,
                    content=str(soup),
                    order_number=index,
                    book=new_book,
                )
                db.session.add(chapter)

            info = f'Succesfully imported file: {efile.title}'
            logging.info(info)
            db.session.commit()
            return info
        else:
            info = 'This Book already exist'
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


def clear_chapters(file):
    raw_content = file.get_content()
    soup = BeautifulSoup(raw_content, 'xml')

    tags_to_clean = [
        'p',
        'h1',
        'h2',
        'h3',
        'h4',
        'span',
        'div',
        'ol',
        'ul',
        'li',
        'section',
    ]

    for tag in soup.find_all(tags_to_clean):
        tag.attrs.pop('class', None)
        tag.attrs.pop('style', None)
        tag.attrs.pop('id', None)

    for index, p_tag in enumerate(soup.find_all('p')):
        p_tag['id'] = f'p-{index}'

    if soup.body:
        return ''.join(str(child) for child in soup.body.children)

    return str(soup)
