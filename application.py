import os

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
    return render_template("index.html")
