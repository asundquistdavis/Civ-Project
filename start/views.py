from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from _thread import start_new_thread
from play.models import Game

def home(request):
    return render(request, 'start/home.html')

@login_required(login_url='/login/')
def newgame(request):
    user = request.user
    if game := user.player.getoradd_game():
        return redirect(f'/newgame/{game.id}')
    else:
        gameid = 0
        return redirect(f'/newgame/{gameid}overwrite/')

@login_required(login_url='/login/')
def newgamebyid(request, gameid=0):
    if request.user.player.current_game.id == gameid:
        return render(request, 'start/newgame.html', {'gameid':gameid})
    else:
        return redirect(f'/newgame/{gameid}/overwrite/')

@login_required(login_url='/login/')
def newgamebyidnext(request, gameid=0):
    user = request.user
    start_new_thread(user.player.current_game.start, ())
    return redirect('/play/')

@login_required(login_url='/login/')
def newgameoverwrite(request, gameid=0):
    return render(request, 'start/newgame.html', {'gameid':gameid, 'overwrite':True})

@login_required(login_url='/login/')
def newgameoverwritenext(request, gameid=0):
    user = request.user
    game = user.player.overwrite_game(gameid=gameid)
    return redirect(f'/newgame/{game.id}/')