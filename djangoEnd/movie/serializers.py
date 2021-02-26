from rest_framework import serializers

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
        fields = ('id', 'title', 'description', 'cover_image', 'genres'
                  )


class MovieSerializer(serializers.ModelSerializer, MovieWatchedSerializer, LikedMoviesSerializer):
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
