import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


# from djangoEnd.movie.models import Movie


class MovieConsumer(WebsocketConsumer):
    groups = ["movie"]

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("movie", self.channel_name)

    def disconnect(self, close_code):
        self.disconnect()
        async_to_sync(self.channel_layer.group_discard)("movie", self.channel_name)

    def receive(self, text_data):
        data = json.loads(text_data)
        type = data["type"].split("_")[1]

        async_to_sync(self.channel_layer.group_send)(
            "movie",
            {
                "type": "movie." + type,
                "text": text_data,
            },
        )

    def movie_comment(self, event):
        self.send(text_data=event["text"])

    def movie_like(self,event):
        self.send(text_data=event["text"])
