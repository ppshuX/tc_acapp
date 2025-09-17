import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tc_acapp.settings')
django.setup()

from game.channelsmiddleware import JwtAuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from game.routing import websocket_urlpatterns


from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddlewareStack(URLRouter(websocket_urlpatterns))
})
