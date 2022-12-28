from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class ExtendedUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(blank=True)
    storage_limit = models.IntegerField(default=10, null = True, blank= True)

    def __str__(self):
        return self.username