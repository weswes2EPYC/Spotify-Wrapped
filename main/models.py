from django.db import models
from user import models as user_models
import uuid

# Create your models here.
class Wrap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(user_models.SpotifyUser, on_delete=models.CASCADE)
    wrap_data = models.JSONField(null=False) # username, tracks, artists, summary
    is_public = models.BooleanField(default=False)

def get_wrap(id):
    wrap = Wrap.objects.get(id=id)
    return wrap

def get_public_wraps():
    return Wrap.objects.filter(is_public=True)