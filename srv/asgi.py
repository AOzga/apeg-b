# Details about what this is and why this file is needed -
# https://channels.readthedocs.io/en/latest/asgi.html


import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "srv.settings")

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from srv import urls


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(urls.websocket_urlpatterns)),
    }
)