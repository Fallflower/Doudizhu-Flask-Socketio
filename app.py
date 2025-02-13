from flask_socketio import emit, join_room, leave_room
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
app = Flask(__name__)


@app.route('/')
def start():  # put application's code here
    return render_template('start.html')


@app.route('/menu.html')
def menu():
    return render_template('menu.html')


@app.route('/login.html')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
