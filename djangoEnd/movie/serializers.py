import urllib.request
import ssl
import os
from pathlib import Path
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers
from .documents.movie import MovieDocument
from .models import Movie, Genre, Comments, WatchedMovies, LikeDislikeOption


class LikedMoviesSerializer():

    def likes_number(self, obj):
        return LikeDislikeOption.objects.filter(movie_id=obj.id, type=True).count()


class MovieWatchedSerializer():

    def has_watched(self, obj):
        user = self.context['request'].user
        return WatchedMovies.objects.filter(movie=obj.id, user=user).exists()


class MovieSerializerPopular(serializers.ModelSerializer, LikedMoviesSerializer):
    likes = serializers.SerializerMethodField('likes_number')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'cover_image', 'genres',
                  'likes')


class ListPhotoSerializer():
    def set_list_photo(self, obj):
        try:
            return get_thumbnailer(obj.cover_image)['list_image'].url
        except:
            return None


class InfoPhotoSerializer():
    def set_info_photo(self, obj):
        try:
            return get_thumbnailer(obj.cover_image)['info_image'].url
        except:
            return None


class MovieRelatedSerializer(serializers.ModelSerializer, InfoPhotoSerializer):
    info_photo = serializers.SerializerMethodField("set_info_photo")

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'cover_image', 'genres', 'image_url_omdb', 'info_photo'
                  )


class MovieSerializer(serializers.ModelSerializer, MovieWatchedSerializer, LikedMoviesSerializer, ListPhotoSerializer,
                      InfoPhotoSerializer):
    watched = serializers.SerializerMethodField('has_watched')
    list_photo = serializers.SerializerMethodField("set_list_photo")
    info_photo = serializers.SerializerMethodField("set_info_photo")

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'cover_image', 'genres',
                  'number_of_views', 'watched', 'image_url_omdb', 'list_photo', 'info_photo')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class WatchedMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedMovies
        fields = '__all__'


class MovieElasticSearchSerializer(DocumentSerializer):
    class Meta(object):
        document = MovieDocument
        fields = (
            'id',
            'title',
            'description',

        )
