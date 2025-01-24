import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Parse the username from the query string
        query_string = parse_qs(self.scope["query_string"].decode())
        self.username = query_string.get("username", ["Anonymous"])[0]  # Default to "Anonymous" if not provided
        self.roomGroupName = "group_chat_gfg"

        # Add the WebSocket connection to the room group
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the room group
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
        # Parse the incoming WebSocket message
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
            }
        )

    async def sendMessage(self, event):
        # Receive the message and username from the room group
        message = event["message"]
        username = event["username"]

        # Send the message back to the WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))
