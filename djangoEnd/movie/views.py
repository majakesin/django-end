from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from .filters import MovieFilter
from .models import Movie, Genre, LikeDislikeOption, Comments, WatchedMovies
from .serializers import MovieSerializer, GenreSerializer, CommentsSerializer, MovieSerializerPopular, \
    MovieRelatedSerializer
from djangoEnd.jwtAuthentication.backends import JWTAuthentication


class PaginationMovie(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CommentsPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10000


class GenreView(mixins.ListModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    pagination_class = PaginationMovie
    filter_class = MovieFilter

    def retrieve(self, request, *args, **kwargs):
        id_movie = kwargs['pk']
        movie = Movie.objects.get(id=id_movie)
        movie.number_of_views = movie.number_of_views + 1
        movie.save()
        serializer = MovieRelatedSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MoviePopularView(mixins.ListModelMixin, GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializerPopular


class RelatedMoviesView(GenericViewSet,mixins.ListModelMixin,):
    queryset = Movie.objects.all()
    serializer_class = MovieRelatedSerializer
    filter_class = MovieFilter



class CommentsView(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin, GenericViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = CommentsPagination

    def get_queryset(self):
        id_movie = self.request.GET['movie']

        if id_movie:
            return Comments.objects.filter(movie=id_movie)
        return Comments.objects()


class LikeDislikeView(GenericAPIView):
    permission_classes = [AllowAny]
    queryset = LikeDislikeOption.objects.all()

    def post(self, request):
        data = request.data;
        user, token = JWTAuthentication.authenticate(self, request)

        if not LikeDislikeOption.objects.filter(user_id=user, movie_id=data['movie_id']).exists():
            ld = LikeDislikeOption()
            ld.movie_id = data['movie_id']
            ld.type = data['type']
            ld.user_id = user
            ld.save()
            return Response(data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get(self, request):
        movie_id = request.GET['movie_id']
        likeList = LikeDislikeOption.objects.filter(movie_id=movie_id, type=True)
        dislikeList = LikeDislikeOption.objects.filter(movie_id=movie_id, type=False)

        data = {
            'likes': likeList.count(),
            'dislikes': dislikeList.count()
        }

        return Response(data, status=status.HTTP_200_OK)


class WatchedMovieView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin, GenericViewSet):
    queryset = WatchedMovies.objects.all()



    def create(self, request, *args, **kwargs):
        movie_id = request.data['movie_id']
        movie = Movie.objects.get(id=movie_id)
        username, token = JWTAuthentication.authenticate(self, request)
        user = User.objects.get(username=username)
        watchedMovie = WatchedMovies()
        watchedMovie.movie = movie
        watchedMovie.user = user
        watchedMovie.save()
        return Response(status=status.HTTP_200_OK)
