import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            # Assume project_id is passed through the URL or scope
            self.project_id = self.scope['url_route']['kwargs']['project_id']
            self.group_name = f'project_{self.project_id}_notifications'
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def send_notification(self, event):
        notification = event["notification"]
        await self.send(text_data=json.dumps({"message": notification}))
