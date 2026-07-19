from livereload import Server
from utils.server_helpers import get_port

from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.debug = True
    server = Server(app.wsgi_app)
    server.watch('templates/')
    server.watch('static/')
    port = get_port(5000)
    server.serve(port)
