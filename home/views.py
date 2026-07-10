from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models import Book, db
from utils.text_helpers import add_epub_file, words_count

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/', methods=['GET', 'POST'])
def index():
    print('CHECK: ', session.get('theme'))
    user_text = ''
    count = 0
    if request.method == 'POST':
        if 'content_text' in request.form:
            user_text = request.form.get('content_text')
            count = words_count(user_text)

        elif 'content_file' in request.files:
            user_file = request.files.get('content_file')
            info = add_epub_file(user_file)
            flash(info)

    all_book = Book.query.all()
    return render_template(
        'home/index.html', user_text=user_text, words_count=count, books=all_book
    )


@home.route('/<int:book_id>/delete_book', methods=['POST'])
def delete_book(book_id):

    book = db.session.scalar(db.select(Book).where(Book.id == book_id))
    if book:
        db.session.delete(book)
        db.session.commit()
        info = 'The Book has been sucessfully deleted'
        flash(info)
    else:
        info = 'EROR. Failed to delete the Book'
        flash(info)
    return redirect(url_for('home.index'))


@home.route('/set_configuration', methods=['POST'])
def set_configuration():
    theme = request.form.get('theme', 'dark')
    interface_font_size = request.form.get('interface-font-size', 16)
    text_font_size = request.form.get('text-font-size', 16)
    container_width = request.form.get('container-width', 60)
    aside_width = request.form.get('aside-width', 210)

    if session.get('theme') != theme:
        session['theme'] = theme
        flash(f'Theme set to {theme}')

    if session.get('interface-font-size') != interface_font_size:
        session['interface-font-size'] = interface_font_size
        flash(f'Interface size set to {interface_font_size}')

    if session.get('text-font-size') != text_font_size:
        session['text-font-size'] = text_font_size
        flash(f'Font size set to {text_font_size}')

    if session.get('container-width') != container_width:
        session['container-width'] = container_width
        flash(f'Container width set to {container_width}')

    if session.get('aside-width') != aside_width:
        session['aside-width'] = aside_width
        flash(f'Aside width set to {aside_width}')

    if (
        request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        or request.is_json
        or 'fetch' in request.headers.get('User-Agent', '').lower()
    ):
        return {'status': 'success'}, 200

    return redirect(request.referrer or url_for('home.index'))
