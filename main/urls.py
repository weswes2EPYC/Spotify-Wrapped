from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('wrapped/', views.spotify_wrapped_view, name='spotify_wrapped'),
]