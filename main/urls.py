from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('my_wraps/', views.wraps_page)
]