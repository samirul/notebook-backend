from django.urls import path
from accounts.consumers import NotificationtConsumer

ws_patterns = [
    path("ws/notifications/<id>/", NotificationtConsumer.as_asgi(), name="notification-consumer"),
]