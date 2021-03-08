from django.urls import re_path

from djangoEnd.consumers import MovieConsumer

websocket_urlpatterns = [
    re_path(r"^ws/movie/consumer/", MovieConsumer.as_asgi()),
]