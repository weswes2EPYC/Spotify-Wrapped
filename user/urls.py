from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup_page),
    path('login', views.login_page),
    path('settings', views.delete_page),
    path('auth/callback', views.handleSpotifyRedirect),
    path('auth/logout', views.handleLogout),
    path('auth/delete', views.handleAccountDelete)
]