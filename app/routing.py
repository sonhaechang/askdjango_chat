from django.urls import path
from app import consumers

websocket_urlpatterns = [
    path('ws/echo/', consumers.EchoConsumer.as_asgi()),
    path('ws/liveblog/', consumers.LiveblogConsumer.as_asgi()),
]