from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chatroom import consumers

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        [
          path('ws/<str:roomname>/', consumers.ChatConsumer.as_asgi()),
            
        ]
    ),
})
