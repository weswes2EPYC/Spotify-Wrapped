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
        'slide1_background': static('Slide1.jpg'),
        'slide2_background': static('Slide2.jpg'),
        'slide4_background': static('Slide4.jpg'),
        'slide6_background': static('Slide6.jpg'),
        'slide8_background': static('Slide8.jpg'),
        'tracks': [
            {
                'name': 'Track One',
                'artist': 'Artist One',
                'album_cover': 'https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228'
            },
            {
                'name': 'Track Two',
                'artist': 'Artist Two',
                'album_cover': 'https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228'
            },
            {
                'name': 'Track Three',
                'artist': 'Artist Three',
                'album_cover': 'https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228'
            }
        ],
        'artists': [
            {
                'name': 'KSI',
                'artist_image': 'https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228'
            },
            {
                'name': 'PlayBoi Carti',
                'artist_image': 'https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228'
            },
            {
                'name': 'Red Hot Chili Peppers',
                'artist_image': 'https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228'
            }
        ],
        'summary': 'lorem ipsium or something idk the rest Lorem ipsum dolor sit amet consectetur adipisicing elit. Molestiae unde dolor maiores a quae exercitationem? Corrupti voluptatibus sapiente quidem voluptatum ea aut beatae explicabo autem maxime iure odit dolor nemo, assumenda perspiciatis adipisci reiciendis, illo nulla praesentium natus, error illum eligendi numquam voluptas. Tempora, tempore dolorem voluptatem corporis molestiae nam a. Quas doloremque consequatur, eum vel dignissimos voluptatum excepturi aspernatur consectetur et maiores totam veniam a facilis qui. Quia ducimus blanditiis, doloremque magni vel nam fugiat odio cupiditate reiciendis quaerat possimus sequi maiores distinctio? Excepturi consequuntur, tempore tempora accusamus quos reprehenderit ullam sit in nam quasi nesciunt inventore exercitationem nisi.'
    }
    
    return render(request, 'main/slideshow.html', {'spotify_data': spotify_data})
