import logging
import zipfile
import base64
import mimetypes
import posixpath
from urllib.parse import unquote
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
        with zipfile.ZipFile(user_file, 'r') as zip:
            container_xml = zip.read('META-INF/container.xml')
            c_root = ET.fromstring(container_xml)
            rootfile = c_root.find('.//container:rootfile', NAMESPACES)
            if rootfile is None:
                raise KeyError
            opf_path = rootfile.attrib['full-path']

            base_dir = opf_path.rsplit(
                '/', 1)[0] + '/' if '/' in opf_path else ''

            opf_content = zip.read(opf_path)
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

                    chapter_content = get_chapters_content(zip, file_zip_path)

                    title = href.rsplit(
                        '/', 1)[-1].replace('.xhtml', '').replace('.html', '')

                    chapter = Chapter(
                        title=title,
                        content=str(chapter_content),
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


def get_chapters_content(zip=None, file_zip_path=''):
    raw_content = zip.read(file_zip_path)
    soup = BeautifulSoup(raw_content, 'html.parser')

    current_dir = posixpath.dirname(file_zip_path)

    for img_tag in soup.find_all(['img', 'image']):
        attr_name = 'src'
        if img_tag.name == 'image':
            if img_tag.has_attr('xlink:href'):
                attr_name = "xlink:href"
            else:
                attr_name = 'href'

        src = img_tag.get(attr_name)

        if not src or src.startswith(('http://', 'https://', 'data:')):
            continue
        img_zip_path = posixpath.normpath(
            posixpath.join(current_dir, unquote(src)))

        try:
            img_bytes = zip.read(img_zip_path)
            b64_str = base64.b64encode(img_bytes).decode('utf-8')

            mime_type, _ = mimetypes.guess_type(img_zip_path)
            if not mime_type:
                mime_type = 'image/png'

            img_tag[attr_name] = f'data:{mime_type};base64,{b64_str}'
        except KeyError:
            info = "Image wasn't found"
            logging.error(info)

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
