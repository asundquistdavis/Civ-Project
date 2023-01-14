from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from _thread import start_new_thread

def home(request):
    return render(request, 'start/home.html')

@login_required()
def newgame(request):
    user = request.user
    if user.player.getoradd_pre_game():
        user.player.getoradd_pre_game()
        return render(request, 'start/newgame.html')
    else:
        return render(request, 'start/newgame.html', {'flag': 'gameinprogress'})

@login_required()
def newgamenext(request):
    user = request.user
    start_new_thread(user.player.game.start, ())
    return redirect('/play/')