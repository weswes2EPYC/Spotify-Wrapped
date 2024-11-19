from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('wrapped/', views.spotify_wrapped_view, name='spotify_wrapped'),
    path("createwrap/", views.create_spotify_wrap, name="createwrap"),
    path("wrap/<str:wrap_id>/", views.view_wrap, name="view_wrap"),
    path('mywraps/', views.myWraps),
    path("create/", views.load_create_page),
    path("delete/<str:wrap_id>/", views.delete_wrap)
]