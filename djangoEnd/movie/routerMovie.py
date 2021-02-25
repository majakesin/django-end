from rest_framework import routers

from .views import MovieView, GenreView, LikeDislikeView

routerMovie = routers.DefaultRouter()
routerMovie.register('movies', MovieView)
routerMovie.register('genres', GenreView)

