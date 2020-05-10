from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    twitter_name = models.CharField(max_length=50)
    twitter_user = models.CharField(max_length=50)
    profile_picture = models.CharField(max_length=100)
    classifier = models.CharField(max_length=100)
    