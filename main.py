from flask_socketio import emit, join_room, leave_room
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash

from app.user import User
from setting import socketio, app


@socketio.on('connect')
def handle_connect():
    sid = request.sid
    print(sid)


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


@app.route('/api/deal_login', methods=['POST'])
def deal_login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        usr = User.check(username, password)
        # print(usr)
        if usr:
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
