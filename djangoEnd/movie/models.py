
from django.contrib.auth.models import User
from django.db import models



def upload_path(instance, filename):
    return '/'.join(['cover_images', str(instance.title), filename])


class LikeDislikeOption(models.Model):
    movie_id = models.IntegerField()
    type = models.BooleanField()
    user_id = models.EmailField()

    class Meta:
        app_label = 'movie'




class Genre(models.Model):
    type = models.CharField(max_length=20)


class Movie(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=600)
    cover_image = models.ImageField(upload_to=upload_path, blank=True)
    image_url_omdb = models.CharField(max_length=1000, null=True)
    genres = models.ManyToManyField(Genre)
    number_of_views = models.IntegerField(default=0)


class Comments(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class WatchedMovies(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
