# from livereload import Server
import threading

from app import app, db

import webview

def start_flask():
    app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    webview.create_window('Epub reader', 'http://127.0.0.1:5001', width=1024, height=768)
    webview.start()

    # app.debug = True
    # server = Server(app.wsgi_app)
    # server.watch('templates/')
    # server.watch('static/')
    # server.serve(port=5000)
    