from flask_socketio import emit, join_room, leave_room
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, session

from app.user import User, uuid
from app.game import Game
from setting import socketio, app, rooms


"""
session includes: 
{
    'logged_in': bool,
    'user': User,       # 登录后
    # 加入房间后：
    'room_id': str(uuid.uuid4())[:4], 
    'player_id': (0|1|2) # 0为创建者，1为第一个加入者，2为第二个
}

rooms includes:
{
    room_id: {
        'name': user defined,
        'game': Game,
        'members': {
            (0|1|2): user dict
        }
        'password': user defined
    },
    ...
}
"""


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


@app.route('/joinRoom.html')
def join_room():
    return render_template('joinRoom.html')


@app.route('/game/<room_id>')
def game(room_id):
    if "room_id" not in session or session["room_id"] != room_id:
        return redirect(url_for('menu'))
    return render_template('game.html', room_id=room_id, room_name=rooms[room_id]['name'])


@app.route('/api/deal_login', methods=['POST'])
def deal_login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        usr = User.check(username, password)
        # print(usr)
        if usr:
            session['user'] = usr
            session['logged_in'] = True
            return jsonify({
                "code": 200,
                "status": True,
                "User": usr
            })

        return jsonify({
            "code": 401,
            "status": False,
            "message": "Invalid Username or Password"
        })


@app.route('/api/deal_create_room', methods=['POST'])
def deal_create_room():
    if request.method == "POST":
        room_id = str(uuid.uuid4())[:4]
        room_name = request.form['roomname']
        room_pwd = request.form['password']

        session['room_id'] = room_id
        session['player_id'] = 0
        rooms[room_id] = {}
        rooms[room_id]['name'] = room_name
        rooms[room_id]['members'] = {0: session['user']['uid']}
        rooms[room_id]['game'] = Game()
        if room_pwd:
            rooms[room_id]['password'] = room_pwd
        else:
            rooms[room_id]['password'] = ''

        return jsonify({
            "code": 200,
            "status": True,
            "room_id": room_id
        })


@app.route('/api/deal_join_room', methods=['POST'])
def deal_join_room():
    if request.method == "POST":
        room_id = request.form['room_id']
        room_pwd = request.form['password']

        if room_pwd == rooms[room_id]['password']:
            player_nums = len(rooms[room_id]['members'])
            rooms[room_id]['members'][player_nums] = session['user']
            session['room_id'] = room_id
            session['player_id'] = player_nums

            return jsonify({
                "code": 200,
                "status": True,
                "room_id": room_id
            })
        return jsonify({
            "code": 401,
            "status": False,
        })


@app.route('/api/deal_logout')
def deal_logout():
    session.pop('user', None)
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
                "code": 201,
                "status": True,
            })
        return jsonify({
            "code": 401,
            "status": False,
            "message": "Username has been taken"
        })


@app.route('/game/get_others_name')
def get_others_info():
    if 'room_id' in session:
        rid = session['room_id']
        pid = session['player_id']
        # 此p1 p2为逻辑上的下家与下下家，并非html中的player1 player2
        p1id = (pid + 1) % 3
        p2id = (pid + 2) % 3
        p1_name = ''
        p2_name = ''
        try:
            p1_name = rooms[rid]['members'][p1id]['name']
            p2_name = rooms[p2id]['members'][p2id]['name']
        except KeyError as e:
            print('Error: ', e)
        finally:
        # p1_card_num = len(rooms[rid]['game'].players[p1id])
        # p2_card_num = len(rooms[rid]['game'].players[p2id])
            return jsonify({
                "code": 200,
                "status": True,
                "player_names": [p2_name, p1_name],
                # "card_nums": [p2_card_num, p1_card_num],
            })

    return jsonify({
        "code": 401,
        "status": False,
        "message": "Error: Room ID not found"
    })


@app.route('/api/verify_room', methods=['POST'])
def verify_room():
    """验证房间信息有效性"""
    data = request.json
    room_id = data.get('room_id')
    # player_id = data.get('player_id')
    uid = session['user'].uid

    # 检查房间是否存在且包含该玩家
    if room_id in rooms and uid in rooms[room_id]['members']:
        return jsonify({'valid': True})
    return jsonify({'valid': False})


@app.route('/game/get_own_cards')
def get_own_cards():
    return jsonify({
        "code": 200,
        "status": True,
        "cards": rooms[session['room_id']]['game'].players[session['player_id']]
    })


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host="192.168.2.188", port=5000)
