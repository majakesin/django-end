from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
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


class MovieRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'cover_image', 'genres','image_url_omdb'
                  )


class MovieSerializer(serializers.ModelSerializer, MovieWatchedSerializer, LikedMoviesSerializer):
    watched = serializers.SerializerMethodField('has_watched')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'cover_image', 'genres',
                  'number_of_views', 'watched','image_url_omdb')


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