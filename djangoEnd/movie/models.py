from enum import Enum

from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    type = models.CharField(max_length=20)


def upload_path(instance, filename):
    return '/'.join(['cover_images', str(instance.title), filename])


class Movie(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=40)
    cover_image = models.ImageField(upload_to=upload_path, blank=True)
    genres = models.ManyToManyField(Genre)
    number_of_views = models.IntegerField(default=0)

class LikeDislikeOption(models.Model):
    movie_id = models.IntegerField()
    type = models.BooleanField()
    user_id = models.EmailField()

