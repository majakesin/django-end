from rest_framework import serializers

from .models import Movie, Genre, Comments, WatchedMovies


class MovieWatchedSerializer():

    def has_watched(self, obj):
        user = self.context['request'].user
        return WatchedMovies.objects.filter(movie=obj.id, user=user).exists()


class MovieSerializer(serializers.ModelSerializer, MovieWatchedSerializer):
    watched = serializers.SerializerMethodField('has_watched')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'cover_image', 'genres',
                  'number_of_views', 'watched')


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
