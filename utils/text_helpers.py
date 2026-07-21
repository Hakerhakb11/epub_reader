import logging
import zipfile
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

from models import Book, Chapter, db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

NAMESPACES = {
    'container': 'urn:oasis:names:tc:opendocument:xmlns:container',
    'opf': 'http://www.idpf.org/2007/opf',
    'dc': 'http://purl.org/dc/elements/1.1/'
}


def words_count(user_text):
    if user_text:
        soup = BeautifulSoup(user_text, 'html.parser')
        if soup.head:
            soup.head.decompose()

        clean_text = soup.get_text(separator=' ')

        words = clean_text.split()
        count = len(words)
        print(f'Количество слов: {count}')
        return count


def add_epub_file(user_file):
    try:
        with zipfile.ZipFile(user_file, 'r') as z:
            container_xml = z.read('META-INF/container.xml')
            c_root = ET.fromstring(container_xml)
            rootfile = c_root.find('.//container:rootfile', NAMESPACES)
            if rootfile is None:
                raise KeyError
            opf_path = rootfile.attrib['full-path']

            base_dir = opf_path.rsplit(
                '/', 1)[0] + '/' if '/' in opf_path else ''

            opf_content = z.read(opf_path)
            opf_root = ET.fromstring(opf_content)

            title_element = opf_root.find('.//dc:title', NAMESPACES)
            book_title = title_element.text if title_element is not None else "Unknown Title"

            new_book = Book.query.filter_by(title=book_title).first()
            if not new_book:
                new_book = Book(title=f'{book_title}')
                db.session.add(new_book)

                manifest = {}
                for item in opf_root.findall('.//opf:item', NAMESPACES):
                    manifest[item.attrib['id']] = item.attrib['href']

                spine_elements = opf_root.findall('.//opf:itemref', NAMESPACES)
                for index, item_spine in enumerate(spine_elements):
                    item_id = item_spine.attrib['idref']
                    href = manifest.get(item_id)
                    if not href:
                        continue

                    file_zip_path = base_dir + href
                    raw_content = z.read(file_zip_path)

                    title = href.rsplit(
                        '/', 1)[-1].replace('.xhtml', '').replace('.html', '')

                    soup = clear_chapters(raw_content)

                    chapter = Chapter(
                        title=title,
                        content=str(soup),
                        order_number=index,
                        book=new_book,
                    )
                    db.session.add(chapter)

                info = f'Succesfully imported file: {book_title}'
                logging.info(info)
                db.session.commit()
                return info
            else:
                info = 'This Book already exist'
                logging.info(info)
                return info

    except (zipfile.BadZipFile, ET.ParseError, KeyError, AttributeError, IndexError):
        info = "Incorrect file type need '.epub'"
        logging.error(info)
        return info


def clear_chapters(raw_content):
    soup = BeautifulSoup(raw_content, 'html.parser')

    tags_to_clean = [
        'p', 'h1', 'h2', 'h3', 'h4', 'span',
        'div', 'ol', 'ul', 'li', 'section',
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
