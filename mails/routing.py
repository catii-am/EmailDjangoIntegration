from django.urls import path
from .consumers import MailConsumer

websocket_urlpatterns = [
    path('ws/mails/', MailConsumer.as_asgi()),
]
