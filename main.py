from flask_socketio import emit, join_room, leave_room
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, session

from app.user import User, uuid
from setting import socketio, app


@socketio.on('connect')
def handle_connect(msg):
    sid = request.sid
    print("received: ", sid)


@app.route('/')
def start():  # put application's code here
    return render_template('start.html')


@app.route('/menu.html')
def menu():
    return render_template('menu.html')


@app.route('/login.html')
def login():
    return render_template('login.html')


@app.route('/register.html')
def register():
    return render_template('register.html')


@app.route('/createRoom.html')
def create_room():
    return render_template('createRoom.html')


@app.route('/game.html')
def game():
    return render_template('game.html')


@app.route('/api/deal_login', methods=['POST'])
def deal_login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        usr = User.check(username, password)
        # print(usr)
        if usr:
            session['username'] = username
            session['logged_in'] = True
            return jsonify({
                "code": 200,
                "status": True,
                "User": usr
            }), 200
        else:
            return jsonify({
                "code": 400,
                "status": False,
                "message": "Invalid Username or Password"
            }), 400


@app.route('/api/deal_create_room', methods=['POST'])
def deal_create_room():
    if request.method == "POST":
        room_id = str(uuid.uuid4())[:4]
        room_name = request.form['roomname']
        room_pwd = request.form['password']

@app.route('/api/deal_logout')
def deal_logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/api/deal_register', methods=['POST'])
def deal_register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        res = User.register(username, password)
        if res:
            return jsonify({
                "code": 200,
                "status": True,
            }), 200
        else:
            return jsonify({
                "code": 401,
                "status": False,
                "message": "Username has been taken"
            }), 401


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host="192.168.2.188", port=5000)
