import ssl
import urllib
from urllib.parse import urlparse

import urllib3
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User

# Create your views here.
from django.core.mail import EmailMessage
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status


from .filters import MovieFilter
from .models import Movie, Genre, LikeDislikeOption, Comments, WatchedMovies
from .serializers import MovieSerializer, GenreSerializer, CommentsSerializer, MovieSerializerPopular, \
    MovieRelatedSerializer
from djangoEnd.jwtAuthentication.backends import JWTAuthentication
from djangoEnd import settings


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


def send_email_fun(subject, content, email_to):
    email = EmailMessage(subject, content, settings.EMAIL_HOST_USER, [email_to,])
    email.fail_silenty = False
    email.send()

def createImageFromUrl(movie,request):
    movie.image_url_omdb = request.POST['cover_image']
    ssl._create_default_https_context = ssl._create_unverified_context
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urllib.request.urlopen(movie.image_url_omdb).read())
    img_temp.flush()
    name = urlparse(movie.image_url_omdb).path.split('/')[-1]
    movie.cover_image.save(name, File(img_temp))

class MovieView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    pagination_class = PaginationMovie
    filter_class = MovieFilter

    def create(self, request, *args, **kwargs):
        title = request.POST['title']
        description = request.POST['description']
        genres = request.POST['genres']
        movieSave = Movie(title=title, description=description)
        movieSave.save()
        movieSave.genres.set(genres)
        try:
            createImageFromUrl(movieSave,request)
        except:
            movieSave.cover_image = request.FILES['cover_image']

        movieSave.save()

        admin = User.objects.get(is_superuser=1)
        content = f"New movie has been created. Movie title is: {title} Movie description is: {description}"
        send_email_fun("Created new movie", content, admin.email)
        return Response(status=status.HTTP_200_OK)

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


class RelatedMoviesView(GenericViewSet, mixins.ListModelMixin, ):
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


#class MovieElasticSearchView(BaseDocumentViewSet):
 #   document = MovieDocument
  #  serializer_class = MovieElasticSearchSerializer
   # lookup_field = 'id'
   # pagination_class = PaginationMovie

   # filter_backends = [
    #    FilteringFilterBackend,
     #   IdsFilterBackend,
      #  OrderingFilterBackend,
       # DefaultOrderingFilterBackend,
       # SearchFilterBackend,
   # ]

    #search_fields = (
     #   'title',
      #  'description',
       # 'genres',
    #)

    #filter_fields = {
     #   'id': {
      #      'field': 'id',
       #     'lookups': [
        #        LOOKUP_FILTER_RANGE,
         #       LOOKUP_QUERY_IN,
          #      LOOKUP_QUERY_GT,
           #     LOOKUP_QUERY_GTE,
            #    LOOKUP_QUERY_LT,
             #   LOOKUP_QUERY_LTE,
           # ],
       # },
       # 'title': 'title.raw',
       # 'description': 'description.raw',

        #'genres': {
         #   'field': 'genres',

          #  'lookups': [
           #     LOOKUP_FILTER_TERMS,
            #    LOOKUP_FILTER_PREFIX,
             #   LOOKUP_FILTER_WILDCARD,
             #   LOOKUP_QUERY_IN,
              #  LOOKUP_QUERY_EXCLUDE,
           # ],
       # },


   # }
  #  ordering_fields = {
    #    'id': 'id',
    #    'title': 'title.raw',
     #   'description': 'description.raw',
   # }
   # ordering =('id',)
