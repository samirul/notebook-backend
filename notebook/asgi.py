import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from middlewares.middleware_channel_auth_jwt import JWTAuthMiddleware
from .routers import ws_patterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notebook.settings')



django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(URLRouter(ws_patterns))
})