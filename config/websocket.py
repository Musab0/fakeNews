# async def websocket_application(scope, receive, send):
#     while True:
#         event = await receive()

#         if event["type"] == "websocket.connect":
#             await send({"type": "websocket.accept"})

#         if event["type"] == "websocket.disconnect":
#             break

#         if event["type"] == "websocket.receive":
#             if event["text"] == "ping":
#                 await send({"type": "websocket.send", "text": "pong!"})














# import json

# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async

# # from .models import Message

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()
    
#     async def disconnect(self, close_code):
#         # Leave room
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
    






