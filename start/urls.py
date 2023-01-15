from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newgame/', views.newgame, name='new game'),
    path('newgame/<int:gameid>/', views.newgamebyid, name='new game by id'),
    path('newgame/<int:gameid>/next/', views.newgamebyidnext, name='new game by id next'),
    path('newgame/<int:gameid>/overwrite/', views.newgameoverwrite, name='new game overwrite'),
    path('newgame/<int:gameid>/overwrite/next/', views.newgameoverwritenext, name='game in progress next'),
]