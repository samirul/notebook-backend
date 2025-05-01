import os
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationtConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__(self)
        self.room_name = os.environ.get("CHANNEL_ROOM_NAME")
        self.room_group_name = f"{os.environ.get("CHANNEL_ROOM_GROUP")}_{self.room_name}"

    async def connect(self):
        await(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        user = self.scope["user"]
        print(user)
        if user.is_authenticated:
            await self.accept()
            await self.send(text_data=json.dumps({"status": "connected"}))
        else:
            await self.close()
            
    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)
    
    async def disconnect(self, code):
        print("disconnected")