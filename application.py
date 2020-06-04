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
            return render_template("error.html")

        usersLogged.append(username)

        session['username'] = Username

        session.permanent = True

        return redirect("/")

    else:
        return render_template("signin.html")            
