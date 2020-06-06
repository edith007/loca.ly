import os
import time

from collections import deque

from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from helpers import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Keep track of channels Created
channelsCreated = []

# Keep track of users Logged
usersLogged = []

# Create a Dictionary
channelsMessages = dict()


@app.route("/")
def index():

    # Saving all the chats in Channel in which user is messaging
    return render_template("index.html", channels=channelsCreated)

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    ''' Save the Username on a Flask session
    after the user submit the sign in form'''

    # Forget any username
    session.clear()

    username = request.form.get("username")

    if request.method == "POST":

        if len(username) < 1 or username is '':
            return render_template("error.html", message="username can't be empty.")

        if username in usersLogged:
            return render_template("error.html", message ="that username already exists!")

        usersLogged.append(username)

        session['username'] = Username

        # Remember the user session on a cookie if the browser if closed.
        session.permanent = True

        # if anything goes wrong redirect to the default route
        return redirect("/")

    else:
        return render_template("signin.html")

@app.route("/logout", methods=['GET'])
def logout():
    """ Logout user from list and delete cookie."""

    try:
        usersLogged.remove(session['username'])
    except ValueError:
        pass

        session.clear()


        return redirect("/")

@app.route("/create", methods=['GET','POST'])
def create():
    """ Create a channel and redirect to its page """

    # Get channel name from form
    newChannel = request.form.get("channel")

    if request.method == "POST":

        if newChannel in channelsCreated:
            return render_template("error.html", message="that channel already exists!")

        # Add channel to global list of channels
        channelsCreated.append(newChannel)

        # Add channel to global dict of channels with messages
        # Every channel is a deque to use popleft() method
        channelsMessages[newChannel] = deque()

        return redirect("/channels/" + newChannel)

    else:

        return render_template("create.html", channels = channelsCreated)

@app.route("/channels/<channel>", methods=['GET', 'POST'])
@login_required
def channel(channel):
    """ Show channels page to send and recieve messages"""

    # Update user current Channel
    session['current_channel'] = channel

    if request.method == "POST":

        return redirect("/")
    else:
        return render_template("channel.html", channels=channelsCreated, messages=channelsMessages[Channel])

@socketio.on("joined", namespace='/')
def joined():
    """ Send meaage to announce that user has entered the channel"""

    room = session.get('current_channel')

    join_room(room)

    emit('status', {
        'userJoined' : session.get('username'),
        'channel': room,
        'msg' : session.get('username') + ' has entered the channel'}
    room=room)

@socketio.on("left", namespace='/')
def left():
    """ Send message to announce that user has left the channel"""

    room = session.get('current_channel')

    leave_room(room)

    emit('status' {
        'msg' : session.get('username') + 'has left the channel'},
        room=room)

       
