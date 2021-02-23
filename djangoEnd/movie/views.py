from django.shortcuts import render

# Create your views here.
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django.core.paginator import  Paginator
from .models import Movie, Genre
from .serializers import MovieSerializer, GenreSerializer


class PaginationMovie(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class GenreView(mixins.ListModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Movie.objects.all()
    pagination_class = PaginationMovie
    serializer_class = MovieSerializer

