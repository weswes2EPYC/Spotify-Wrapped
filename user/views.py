from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseForbidden, HttpResponseBadRequest
import base64
import os
import json
from django.views.decorators.http import require_http_methods, require_GET
import requests
import datetime
import math
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import SpotifyUser
from django.core.serializers.json import DjangoJSONEncoder



SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Create your views here.
@require_GET
def signup_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    return render(request, "user/signup.html")

@require_GET
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    return render(request, "user/login.html")

@require_GET
def handleSpotifyRedirect(request):
    query_params = dict(request.GET)
    if "code" not in query_params:
        return redirect("/") # just redirect without login
    
    request_body = {
        "code": query_params["code"],
        "redirect_uri": "http://127.0.0.1:8000/auth/callback", # change this when in production
        "grant_type": "authorization_code"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64.urlsafe_b64encode(bytes(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}", "utf-8")).decode()}"
    }
    verify_token_response = requests.post("https://accounts.spotify.com/api/token", data=request_body, headers=headers) # i believe this is synchronous
    if verify_token_response.status_code != 200:
        return redirect("/") # again, just redirect to home page
    verify_token_json = verify_token_response.json()

    access_token = verify_token_json["access_token"]
    refresh_token = verify_token_json["refresh_token"]
    expires_in = verify_token_json["expires_in"] - 300
    expires_at = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)

    get_user_response = requests.get("https://api.spotify.com/v1/me", headers={
        "Authorization": f"Bearer {access_token}"
    })
    if get_user_response.status_code != 200:
        return redirect("/")
    get_user_json = get_user_response.json()
    email = get_user_json["email"]


    user = authenticate(email=email)
    if user is None:
        user = SpotifyUser.objects.create(email=email)
    login(request, user) # refresh the session
    session = request.session
    session["access_token"] = access_token
    session["expires_at"] = expires_at.timestamp()
    session["refresh_token"] = refresh_token
    session.save()



    return redirect("/")

@require_GET
def handleLogout(request):
    try:
        logout(request)
    except:
        pass
    return redirect("/")