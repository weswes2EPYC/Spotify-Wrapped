from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('wrapped', views.spotify_wrapped_view, name='spotify_wrapped'),
    path("createwrap", views.create_spotify_wrap, name="createwrap"),
    path("wrap/<uuid:wrap_id>", views.view_wrap, name="view_wrap")
]