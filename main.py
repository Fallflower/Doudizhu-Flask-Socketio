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
    'player_id': (0|1|2) # 创建者为0，第一个加入者为1，第二个为2
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


@socketio.on('connect')
def handle_connect():
    # if 'user' not in session or 'room_id' not in session or session['room_id'] not in rooms:
    #     return
    # join_room(session['room_id'])
    # emit('room_update', {
    #     'members': rooms[session['room_id']]['members'],
    #     'room_name': rooms[session['room_id']]['name'],
    # }, room=session['room_id'])
    print('connected')


@socketio.on('disconnect')
def handle_disconnect():
    # if 'room_id' not in session:
    #     return
    #
    # room_id = session['room_id']
    # player_id = session['player_id']
    #
    # if room_id in rooms:
    #     if player_id in rooms[room_id]['members']:
    #         del rooms[room_id]['members'][player_id]
    #
    #         # 如果房间为空则删除房间
    #         if not rooms[room_id]['members']:
    #             del rooms[room_id]
    #         else:
    #             emit('member_left', {
    #                 'player_id': player_id,
    #                 'remaining_members': rooms[room_id]['members'],
    #             })
    print('disconnected')
    # leave_room(room_id)
    # session.pop('room_id', None)
    # session.pop('player_id', None)


@socketio.on('create_room')
def handle_create_room(data):
    room_name = data['name']
    password = data.get('password', '')
    room_id = str(uuid.uuid4())[:4]

    rooms[room_id] = {
        'name': room_name,
        'password': password,
        'members': {0: session['user']},
        'game': Game(),
    }
    # 更新会话
    session['room_id'] = room_id
    session['player_id'] = 0

    emit('room_created', {
        'room_id': room_id,
    })
    session['in_room'] = True


@socketio.on('join_room')
def handle_join_room(data):
    room_id = data['room_id']
    password = data.get('password', '')

    if room_id not in rooms or password != rooms[room_id]['password']:
        emit('join_failed', {'message': 'Invalid RoomID or Password'})
        return
    # 判断是否已在房间中
    if 'player_id' in session \
            and session['player_id'] in rooms[room_id]['members'] \
            and session['user'] == rooms[room_id]['members'][session['player_id']]:
        emit('join_success', {'room_id': room_id})
    # 分配玩家id
    player_id = len(rooms[room_id]['members'])
    if player_id >= 3:
        emit('join_failed', {'message': 'Room is FULL'})
        return

    if not session['in_room']:
        # 更新房间数据
        rooms[room_id]['members'][player_id] = session['user']
        session['room_id'] = room_id
        session['player_id'] = player_id
        session['in_room'] = True

    emit('join_success', {
        'room_id': room_id,
    })


@socketio.on('rejoin_room')  # 由于从joinRoom页面跳转到game页面的socket连接变化，进入game页面重连
def handle_rejoin_room(data):
    if 'room_id' not in session:
        session['in_room'] = False
        return
    elif session['room_id'] not in rooms:
        session['in_room'] = False  # 防止浏览器报错了老session值
        return
    if 'player_id' not in session:
        return
    room_id = session['room_id']
    player_id = session['player_id']
    members = rooms[room_id]['members']
    for key, _ in rooms[room_id]['members'].items():
        members[key]['card_num'] = len(rooms[room_id]['game'].players[key])
    print("room: ", room_id, "\tmembers: ", members)
    join_room(room_id)
    emit('member_joined', {
        'player_id': player_id,
        'members': members
    }, room=room_id)
    if data['apply']:
        emit('join_success', {
            'room_id': room_id,
        })


@app.route('/')
def start():
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
def _create_room():
    return render_template('createRoom.html')


@app.route('/joinRoom.html')
def _join_room():
    return render_template('joinRoom.html')


@app.route('/game/<room_id>')
def game(room_id):
    # if "room_id" not in session or session["room_id"] != room_id:
    #     return redirect(url_for('menu'))
    if "in_room" in session and session['in_room']:
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


@app.route('/api/verify_room', methods=['POST'])
def verify_room():
    """验证房间信息有效性"""
    data = request.json
    room_id = data.get('room_id')
    # player_id = data.get('player_id'
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


@app.route('/game/get_own_view')
def get_own_view():
    return jsonify({
        "code": 200,
        "status": True,
        "player_id": session['player_id']
    })


if __name__ == '__main__':
    socketio.run(
        app,
        debug=True,
        allow_unsafe_werkzeug=True,
        host="0.0.0.0",
        port=5000,
        # certfile='localhost.pem',
        # keyfile='localhost-key.pem'
    )
