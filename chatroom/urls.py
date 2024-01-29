from django.urls import path
from .views import *

urlpatterns = [
    path('',chatroom , name="chatroom"),
    path('roompage/',roomboard , name="roompage"),
    path('base/',base , name="base"),
    path('<slug:slug>/', room, name="room"),
    
    
]