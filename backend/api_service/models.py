from django.db import models

# Create your models here.
class Character(models.Model):
    name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    hairColor = models.CharField(max_length=255)
    eyeColor = models.CharField(max_length=255)