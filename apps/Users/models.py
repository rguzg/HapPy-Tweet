from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # twitter_name = models.CharField(max_length=50)
    # twitter_user = models.CharField(max_length=50)
    twitter_id = models.CharField(max_length=20)
    # profile_picture = models.CharField(max_length=100)
    # profile_banner = models.CharField(max_length=100)

class Classifier(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    shortened_name = models.CharField(max_length=2)
    