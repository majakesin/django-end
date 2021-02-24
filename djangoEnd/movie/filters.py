from django_filters import NumberFilter, FilterSet, CharFilter

from .models import Movie


class MovieFilter(FilterSet):
    movie_search = CharFilter(field_name="title",lookup_expr="icontains")
    genre = NumberFilter(field_name="genres",lookup_expr="exact")

    class Meta:
        model = Movie
        fields = ('movie_search','genre')