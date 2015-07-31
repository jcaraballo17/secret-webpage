from django.db import models


class HomePageImage(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='home_images')


class Announcement(models.Model):
    title = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    short_description = models.CharField(max_length=1024)
    active = models.BooleanField(default=True)


class Piece(models.Model):
    title = models.CharField(max_length=256)
    date = models.DateField()
    description = models.CharField(max_length=512)
    size = models.CharField(max_length=32)
    medium = models.CharField(max_length=128)
