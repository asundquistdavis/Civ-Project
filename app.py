from _thread import start_new_thread
from flask import Flask, render_template, Blueprint, redirect, url_for
from flask_socketio import SocketIO
from time import sleep
from game.game import Game

app = Flask(__name__)
app.config['SECRET_KEY'] = '###afshd&&!2'
socket = SocketIO(app)

@socket.on('message')
def handle_message(data):
    print('received message: ' + data)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/play')
def play():
    return render_template('/play')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/logout')
def logout():
    return redirect('/')

if __name__ == '__main__':
    socket.run(app)