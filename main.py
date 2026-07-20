import sys

from app import app, db
from utils.server_helpers import get_port


def start_flask(port):
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    port = get_port(5000)
    if '--dev' in sys.argv:
        from livereload import Server
        app.debug = True
        server = Server(app.wsgi_app)
        server.watch('templates/')
        server.watch('static/')
        server.serve(port)

    else:
        import threading

        import webview
        flask_thread = threading.Thread(target=start_flask, args=(port,))
        flask_thread.daemon = True
        flask_thread.start()

        webview.create_window(
            'Epub reader', f'http://127.0.0.1:{port}', width=1024, height=768)
        webview.start()
