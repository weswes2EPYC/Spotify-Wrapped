from django.utils.deprecation import MiddlewareMixin
import datetime
import requests
from django.contrib.auth import authenticate, login


class SpotifySessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            session = request.session
            print("MIDDLE WARE PROCESSED")
            if "access_token" not in session:
                print("NOT LOGGED IN")
                # request.user.is_authenticated = False
                return
            
            # If not expires, then we can try to call
            if session["expires_at"] > datetime.datetime.now().timestamp():
                request.user.is_authenticated = True
            else:
                print("expired")
                # If expired, then need to refresh token
                refresh_token_response = requests.post("https://accounts.spotify.com/api/token", data={
                    "grant_type": "refresh_token",
                    "refresh_token": session["refresh_token"]
                }, headers = {
                    "Content-Type": "application/x-www-form-urlencoded"
                })

                if refresh_token_response.status_code != 200:
                    request.user.is_authenticated = False
                    return

                refresh_token_json = refresh_token_response.json()
                access_token = refresh_token_json["access_token"]
                expires_in = refresh_token_json["expires_in"]-300 # make sure to refresh 5 minutes early
                new_refresh_token = refresh_token_json["refresh_token"]
                expires_at = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
                login(request, request.user) # refresh the session
                session["access_token"] = access_token
                session["expires_at"] = expires_at.timestamp()
                session["refresh_token"] = new_refresh_token

                session.save()

                request.user.is_authenticated = True
        except:
            request.user.is_authenticated = False