from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'start/home.html')

@login_required()
def newgame(request):
    user = request.user
    if user.player.getoradd_pre_game():
        user.player.getoradd_pre_game()
        return render(request, 'start/newgame.html', {'login': True})
    else:
        return render(request, 'start/newgame.html', {'flag': 'gameinprogress', 'login': True})
