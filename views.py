from app import app
from flask import render_template, request
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub


@app.route('/', methods=['GET', 'POST'])
def index():
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
            user_file = request.files.get('fontent_file')
            efile = epub.read_epub(user_file)
            print(efile)
            print(efile.get_items_of_type(ebooklib.ITEM_UNKNOWN))
            print("EAZY")

    return render_template('index.html', user_text=user_text, words_count=count)
