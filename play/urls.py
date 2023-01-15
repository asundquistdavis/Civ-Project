from django.urls import path
from . import views

urlpatterns = [
    path('', views.play, name='play'),
    path('endgame/', views.endgame, name='end game'),
    path('board/', views.board, name='board'),
]