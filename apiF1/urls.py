from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('drivers/<int:driver_id>/', views.api_driver),
    path('teams/<int:team_id>/', views.api_team),
    path('drivers/', views.api_drivers),
    path('teams/', views.api_teams),
    path('token/', views.api_get_token),
    path('users/', views.api_user),
]