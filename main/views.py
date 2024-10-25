from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET
from django.templatetags.static import static

# Create your views here.
@require_GET
def home_page(request):
    return render(request, "main/home.html", {})

def spotify_wrapped_view(request):
    # Dummy Spotify data
    spotify_data = {
        'username': 'eskedie',
        'tracks': [
            {
                'name': 'Track One',
                'artist': 'Artist One',
                'album_cover': static('Slide1.jpg')
            },
            {
                'name': 'Track Two',
                'artist': 'Artist Two',
                'album_cover': 'https://via.placeholder.com/600x800.png?text=Album+Cover+2'
            }
        ]
    }
    
    return render(request, 'main/slideshow.html', {'spotify_data': spotify_data})
