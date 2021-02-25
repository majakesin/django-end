from rest_framework import routers

from .views import MovieView, GenreView, CommentsView

routerMovie = routers.DefaultRouter()
routerMovie.register('movies', MovieView)
routerMovie.register('genres', GenreView)
routerMovie.register('comments', CommentsView)
