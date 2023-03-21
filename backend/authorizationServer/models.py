from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CharacterSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    hairColor = models.CharField(max_length=255)
    eyeColor = models.CharField(max_length=255)
