from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os

login_required(login_url='/login/')
def play(request):
    return render(request, 'play/game.html')

login_required(login_url='/login/')
def endgame(request):
    request.user.player.current_game.delete()
    return redirect('/newgame/')

def board(request):
    board = open(os.path.join(os.path(__file__), 'static/assets/board.geojson'))
    return board