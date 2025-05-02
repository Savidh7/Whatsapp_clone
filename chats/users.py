import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "watsapp.settings")
import django
django.setup()
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from asgiref.sync import sync_to_async

@sync_to_async
def get_user_by_username(username): return User.objects.get(username=username)

class ChatUser(AsyncWebsocketConsumer):
    async def connect(self):
        # Chat name
        self.other_user = self.scope['url_route']['kwargs']['username']
        self.current_user = self.scope['user']
        users = sorted([self.current_user.username, self.other_user])
        self.chat_name = f"chat_{users[0]}_{users[1]}"

        # Join chat
        await self.channel_layer.group_add(
            self.chat_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        sender = self.scope['user']
        receiver = await get_user_by_username(self.other_user)
        await self.save_message(sender, receiver, message)

        # Send message in chat
        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @staticmethod
    @sync_to_async
    def save_message(sender, receiver, message):
        Message.objects.create(sender=sender, receiver=receiver, message=message)