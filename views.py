from app import app
from flask import render_template, request

@app.route('/', methods = ['GET', 'POST'])
def index():
    user_text = ""
    if request.method == 'POST':
        user_text = request.form.get('content')
    return render_template('index.html', text=user_text)
