import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from flask_socketio import SocketIO, join_room, leave_room, send,emit


# Configure app
app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
socketio = SocketIO(app, manage_session=False)

# Predefined rooms for chat
ROOMS = ["General","Important" , "Random"]
users = {}

@app.route("/", methods=['GET'])
def chat():
    return render_template("chat.html",rooms=ROOMS)
    # username =  request.form.get('name')

@app.route("/channel")
def channel():
    return render_template('channel.html')

@app.route("/", methods=['POST'])
def newchannel():
    Newchannel =  request.form.get('channelname')


    if Newchannel not in ROOMS:
        ROOMS.append(Newchannel)
    elif Newchannel in ROOMS:
        flash('Channel With Same Name Already Exists')

    return render_template("chat.html",rooms=ROOMS)

@app.route("/private")
def private():
    return render_template('private.html')

@app.route("/username", methods=["POST"])
def username():
    username = request.form.get("username")
    if username is None:
        return jsonify({"success": False})
    return jsonify({"success": True, "username":username} )


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@socketio.on('incoming-msg')
def on_message(data):
    """Broadcast messages"""

    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    # Set timestamp
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)

@socketio.on('join')
def on_join(data):
    """User joins a room"""

    username = data["username"]
    room = data["room"]
    join_room(room)

    # Broadcast that new user has joined
    send({"msg": username + " has joined the " + room + " channel."}, room=room)

@socketio.on('leave')
def on_leave(data):
    """User leaves a room"""

    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " has left the channel"}, room=room)

@socketio.on('username', namespace='/private')
def receive_username(username):
    users[username] = request.sid
    #users.append({username : request.sid})
    #print(users)
    print('Username added!')

@socketio.on('private_message', namespace='/private')
def private_message(payload):
    recipient_session_id = users[payload['username']]
    message = payload['message']
    sender = payload['sender']
    emit('new_private_message',{"sender": sender, "message": message}, room=recipient_session_id)



if __name__ == "__main__":
    app.run(debug=True)
