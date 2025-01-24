import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
      
        query_string = parse_qs(self.scope["query_string"].decode())
        self.username = query_string.get("username", ["Anonymous"])[0]
        self.recipient = query_string.get("recipient", [None])[0]  

        if self.recipient:
           
            users = sorted([self.username, self.recipient])  
            self.roomGroupName = f"personal_chat_{users[0]}_{users[1]}"
        else:
            self.roomGroupName = "group_chat"

        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
       
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
 
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        username = text_data_json.get("username")

        await self.channel_layer.group_send(
            self.roomGroupName,
            {
                "type": "sendMessage",
                "message": message,
                "username": username,
            }
        )

    async def sendMessage(self, event):
       
        message = event["message"]
        username = event["username"]

      
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))
