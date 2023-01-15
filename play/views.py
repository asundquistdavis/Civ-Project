from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from pathlib import Path
import os
from json import load

@login_required(login_url='/login/')
def playgame(request):
    return render(request, 'play/game.html')

@login_required(login_url='/login/')
def endgame(request):
    request.user.player.current_game.delete()
    return redirect('/newgame/')

def territories(request):
    with open(os.path.join(Path(__file__).parent, 'static', 'play', 'assets', 'territories.geojson'), 'r') as territories: 
        return JsonResponse(load(territories))

def board(request):
    with open(os.path.join(Path(__file__).parent, 'static', 'play', 'assets', 'board.geojson'), 'r') as board:
        return JsonResponse(load(board))

def getgame(request):
    game = request.user.player.current_game
    return JsonResponse(load(board))