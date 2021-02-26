from rest_framework import routers

from .views import MovieView, GenreView, CommentsView, WatchedMovieView

routerMovie = routers.DefaultRouter()
routerMovie.register('movies', MovieView)
routerMovie.register('genres', GenreView)
routerMovie.register('comments', CommentsView)
routerMovie.register('watched', WatchedMovieView)
