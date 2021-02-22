from rest_framework import routers

from .views import MovieView, GenreView

routerMovie = routers.DefaultRouter()
routerMovie.register('movies', MovieView)
routerMovie.register('genres', GenreView)
