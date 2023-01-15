from django.urls import path
from . import views

urlpatterns = [
    path('', views.playgame, name='play'),
    path('endgame/', views.endgame, name='end game'),
    path('territories', views.territories, name='territories'),
    path('board/', views.board, name='board'),
    path('getgame', views.getgame, name='get game object')
]