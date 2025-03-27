from flask_socketio import SocketIO
from flask import Flask

from app.user import User


User.load()
app = Flask(__name__)
app.secret_key = "FEICHANGANQUANDEMIYAO"
socketio = SocketIO(app)
