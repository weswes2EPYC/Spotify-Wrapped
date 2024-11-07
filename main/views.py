from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_GET
from django.templatetags.static import static
import requests
import time
import datetime
import base64
import os

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

@require_GET
def home_page(request):
    return render(request, "main/home.html", {})