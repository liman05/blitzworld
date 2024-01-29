from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?p<chatroom>\w+)/$', consumer.ChatConsumer),
    # path('ws/<str:roomname>/', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/room/(?P<roomname>\w+)/$', consumers.ChatConsumer.as_asgi()),

]
