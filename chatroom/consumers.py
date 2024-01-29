import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import *
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
       async def connect(self):
              self.roomname = self.scope['url_route']['kwargs']['roomname']
              self.chatroom_group = 'chat_%s'% self.roomname

              await self.channel_layer.group_add(
                     self.chatroom_group,
                     self.channel_name
              )
              await self.accept()

       async def disconnect(self):
              await self.channel_layer.group_discard(
                     self.chatroom_group,
                     self.channel_name
              )

       async def receive(self, text_data):
               data = json.loads(text_data)
               message = data['message']
               username = data['username']
              #  room = data['roomName']
               room = data.get('room', None)

               await self.save_massage(username,room,message)

               await self.channel_layer.group_send(
                  self.chatroom_group,
                  {
                         'type':'chat_message',
                         'message': message,
                         'username': username,
                         'room': room,
                  }
              )
               
       async def chat_message(self, event):
               message = event['message']
               username = event['username']
               room = event['room']

               await self.send(text_data = json.dumps({
                      'message': message,
                      'username': username,
                      'room': room,
               }))

       @sync_to_async
       def save_massage(self, username, room, message):
              user = User.objects.get(username=username)
              room = Room.objects.get(slug=room)

              Massage.objects.create(user=user, room=room, content=message)



          
  
   
