from django.contrib.auth.backends import ModelBackend
from .models import SpotifyUser

class SpotifyAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = SpotifyUser.objects.get(email=email)
            
            return user
        except SpotifyUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return SpotifyUser.objects.get(pk=user_id)
        except SpotifyUser.DoesNotExist:
            return None