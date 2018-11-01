from channels.routing import ProtocolTypeRouter, URLRouter
import weather.routing


application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": URLRouter(weather.routing.websocket_urlpatterns)
    }
)
