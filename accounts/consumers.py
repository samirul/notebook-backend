import os
import json
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer
from .token_checker import check_token

class NotificationtConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__(self)
        self.room_name = None
        self.room_group_name = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f"{os.environ.get("CHANNEL_ROOM_GROUP")}_{self.room_name}"
        await(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        user = self.scope["user"]

        if user.is_authenticated and self.room_name == str(user.id):
            await self.accept()
            await self.send(text_data=json.dumps({"status": "connected"}))
        else:
            await self.close()
            
    async def receive(self, text_data=None, bytes_data=None):
        user = await check_token(self.scope["headers"])
        if isinstance(user, AnonymousUser):
            await self.close()
            return
        
        await(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_notification_created_category',
                'notification': text_data
            }
        )
    
    async def disconnect(self, code):
        print("disconnected")


    async def send_notification_created_category(self, event):
        value = event.get('notification')
        await self.send(text_data=json.dumps({
            'notification': value
        }))