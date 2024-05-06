import time
import threading
import webbrowser
from flask import Flask
from router import create_routes
from database.db import create_database

app = Flask(__name__, template_folder='templates', static_folder='static')

create_routes(app)

def open_browser():
    time.sleep(5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == "__main__":
    create_database()
    threading.Thread(target=open_browser).start()
    app.run()
