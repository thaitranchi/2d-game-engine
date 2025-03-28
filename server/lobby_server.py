import os
from flask import Flask, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersekrit')
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}

# ------------------------- SocketIO Events ------------------------- #

@socketio.on('connect')
def on_connect():
    print(f"[CONNECTED] Client connected with SID {request.sid}")

@socketio.on('create_room')
def handle_create_room(data):
    room = data.get('room')
    if not room:
        emit('error', {'error': 'Room name is required.'})
        return
    if room not in rooms:
        rooms[room] = []
    if request.sid not in rooms[room]:
        join_room(room)
        rooms[room].append(request.sid)
        print(f"[ROOM CREATED] {room} by {request.sid}")
        emit('room_created', {'room': room}, room=room)

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data.get('room')
    if room in rooms and request.sid in rooms[room]:
        leave_room(room)
        rooms[room].remove(request.sid)
        print(f"[LEFT ROOM] {request.sid} left {room}")
        emit('room_left', {'room': room}, room=room)

@socketio.on('chat_message')
def handle_chat_message(data):
    room = data.get('room')
    message = data.get('message')
    if room in rooms:
        print(f"[MESSAGE] {request.sid} to {room}: {message}")
        emit('chat_message', {'sid': request.sid, 'message': message}, room=room)

@socketio.on('disconnect')
def on_disconnect():
    for room, sids in rooms.items():
        if request.sid in sids:
            sids.remove(request.sid)
            print(f"[DISCONNECTED] {request.sid} left {room}")

# ------------------------- Run Application ------------------------- #

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
