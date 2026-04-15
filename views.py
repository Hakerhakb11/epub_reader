from app import app
from flask import render_template, request
from bs4 import BeautifulSoup



@app.route('/', methods = ['GET', 'POST'])
def index():
    user_text = ""
    count = 0
    if request.method == 'POST':
        user_text = request.form.get('content')
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

    return render_template('index.html', user_text=user_text, words_count=count)
