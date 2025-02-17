from flask_socketio import SocketIO
from flask import Flask

from app.user import User


User.load()
app = Flask(__name__)
socketio = SocketIO(app)
