from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newgame/', views.newgame, name='new game'),
    path('newgame/next/', views.newgamenext, name='new game next'),
]