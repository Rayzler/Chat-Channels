import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from roomApp.models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None

    async def connect(self):
        self.room_name = self.scope['path'].strip('/ws/')
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def get_channel_name(self):
        return self.channel_name

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]
        room = data["room"]

        await self.save_messages(username, room, message)

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "send_message",
                "message": message,
                "username": username,
                "room": room
            })

    async def send_message(self, event):
        username = event["username"]
        room = event["room"]
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message, "username": username, "room": room}))

    @sync_to_async
    def save_messages(self, username, room, message):
        _user = User.objects.get(username=username)
        _room = Room.objects.get(slug=room)

        Message.objects.create(user=_user, room=_room, content=message)
