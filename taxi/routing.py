from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from trips.consumer import TaxiConsumer

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(
            [
                path("taxi/", TaxiConsumer.as_asgi()),
            ]
        ),
    }
)
