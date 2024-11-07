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

def get_valid_access_token(request):
    access_token = request.session.get('access_token')
    expires_at = request.session.get('expires_at', 0)

    if not access_token or time.time() > expires_at:
        # Token is expired or missing, refresh it
        access_token = refresh_access_token(request)
    return access_token

def refresh_access_token(request):
    refresh_token = request.session.get('refresh_token')
    if not refresh_token:
        # Redirect to login if refresh token is not available
        return None
    
    request_body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64.urlsafe_b64encode(bytes(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}', 'utf-8')).decode()}"
    }
    response = requests.post("https://accounts.spotify.com/api/token", data=request_body, headers=headers)
    if response.status_code != 200:
        return None
    response_json = response.json()
    access_token = response_json["access_token"]
    expires_in = response_json["expires_in"] - 300
    expires_at = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
    request.session["access_token"] = access_token
    request.session["expires_at"] = expires_at.timestamp()
    request.session.save()
    return access_token

@require_GET
def spotify_wrapped_view(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    access_token = get_valid_access_token(request)
    if not access_token:
        return redirect('/auth/login')

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Fetch User Profile
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    if response.status_code != 200:
        return redirect('/auth/login')
    user_profile = response.json()
    username = user_profile.get('display_name', 'Unknown User')

    # Fetch Top Tracks
    params = {
        'limit': 3,
        'time_range': 'long_term'
    }
    response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers, params=params)
    if response.status_code != 200:
        return redirect('/auth/login')
    top_tracks = response.json().get('items', [])

    # Process Tracks Data
    tracks = []
    for track in top_tracks:
        track_info = {
            'name': track['name'],
            'artist': ', '.join([artist['name'] for artist in track['artists']]),
            'album_cover': track['album']['images'][0]['url'] if track['album']['images'] else static('default_album_cover.jpg')
        }
        tracks.append(track_info)

    # Fetch Top Artists
    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers, params=params)
    if response.status_code != 200:
        return redirect('/auth/login')
    top_artists = response.json().get('items', [])

    # Process Artists Data
    artists = []
    for artist in top_artists:
        artist_info = {
            'name': artist['name'],
            'artist_image': artist['images'][0]['url'] if artist['images'] else static('default_artist_image.jpg')
        }
        artists.append(artist_info)

    # Prepare Spotify Data
    spotify_data = {
        'username': username,
        'slide1_background': static('Slide1.jpg'),
        'slide2_background': static('Slide2.jpg'),
        'slide4_background': static('Slide4.jpg'),
        'slide6_background': static('Slide6.jpg'),
        'slide8_background': static('Slide8.jpg'),
        'tracks': tracks,
        'artists': artists,
        'summary': 'Your Spotify Wrapped Summary'
    }

    return render(request, 'main/slideshow.html', {'spotify_data': spotify_data})
