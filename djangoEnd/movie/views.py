from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from .models import Movie, Genre
from .serializers import MovieSerializer, GenreSerializer


class GenreView(mixins.ListModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
