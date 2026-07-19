from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models import Book, Config, db
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
    bg_color = request.form.get('bg-color', '#121212')
    text_color = request.form.get('text-color', '#e0e0e0')
    font_family = request.form.get('font-family', 'default')
    interface_font_size = request.form.get('interface-font-size', 16, type=int)
    text_font_size = request.form.get('text-font-size', 16, type=int)
    container_width = request.form.get('container-width', 60, type=int)
    aside_width = request.form.get('aside-width', 210, type=int)
    paragraph_spacing = request.form.get('paragraph-spacing', 15, type=int)

    new_config = {
        'bg-color': bg_color,
        'text-color': text_color,
        'font-family': font_family,
        'interface-font-size': interface_font_size,
        'text-font-size': text_font_size,
        'container-width': container_width,
        'aside-width': aside_width,
        'paragraph-spacing': paragraph_spacing
    }

    session['config'] = new_config

    config = db.session.scalar(db.select(Config).order_by(Config.id.desc()))
    if config:
        config.config_json = new_config
    else:
        config = Config(config_json=new_config)
        db.session.add(config)
    db.session.commit()

    if (
        request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        or request.is_json
        or 'fetch' in request.headers.get('User-Agent', '').lower()
    ):
        return {'status': 'success'}, 200

    return redirect(request.referrer or url_for('home.index'))


@home.before_app_request
def load_config():
    if 'config' not in session:
        config = db.session.scalar(db.select(Config).order_by(Config.id.desc()))
        if config:
            session['config'] = config.config_json
        else:
            default_config = {
                'bg-color': '#121212',
                'text-color': '#e0e0e0',
                'font-family': 'default',
                'interface-font-size': 16,
                'text-font-size': 16,
                'container-width': 60,
                'aside-width': 210,
                'paragraph-spacing': 15
            }

            session['config'] = default_config

            db.session.add(Config(config_json=default_config))
            db.session.commit()
