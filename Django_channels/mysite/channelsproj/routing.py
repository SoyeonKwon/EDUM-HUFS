from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from notifier.consumers import CamConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("notifications/", CamConsumer),
    ])
})

ASGI_APPLICATION = "Channelsproj.routing.application"


