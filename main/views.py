from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET

# Create your views here.
@require_GET
def home_page(request):
    return render(request, "main/home.html", {})

def wraps_page(request):
    user_data = {
        'username': 'eskedie',
        'wraps': []
    }
    return render(request, "main/my_wraps.html", {'user': user_data})