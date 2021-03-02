from rest_framework import routers

from .views import MovieView, GenreView, CommentsView, WatchedMovieView, MoviePopularView, RelatedMoviesView, \
    MovieElasticSearchView

routerMovie = routers.DefaultRouter()
routerMovie.register('movies', MovieView)
routerMovie.register('genres', GenreView)
routerMovie.register('comments', CommentsView)
routerMovie.register('watched', WatchedMovieView)
routerMovie.register('popular', MoviePopularView)
routerMovie.register('related',RelatedMoviesView)
routerMovie.register('search', MovieElasticSearchView, basename="moviedocument")