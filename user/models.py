from django.db import models
from django.contrib.sessions.models import Session
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# Create your models here.
class SpotifyUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.TextField(null=False)
    is_authenticated = models.BooleanField(default=False)
    REQUIRED_FIELDS=[]
    USERNAME_FIELD='email'

    def __str__(self):
        return self.email