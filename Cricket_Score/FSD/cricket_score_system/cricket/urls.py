# cricket/urls.py

from django.urls import path
from . import views # Imports your views from the same app

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.team_list, name='team_list'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
    path('player/<int:player_id>/', views.player_stats, name='player_stats'),
    path('player/<int:player_id>/matches/', views.player_full_match_history, name='player_full_match_history'),
    path('matches/', views.all_matches, name='all_matches'),
]
