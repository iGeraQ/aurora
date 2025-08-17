from django.urls import re_path
from apps.voice.consumers import VoiceConsumer

websocket_urlpatterns = [
    re_path(r"ws/voice/$", VoiceConsumer.as_asgi()),
]