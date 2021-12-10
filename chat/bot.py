from channels.generic.websocket import AsyncConsumer, AsyncWebsocketConsumer


class BotConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, event):
        self.name = self.scope["url_route"]["kwargs"]["name"]

        # add user into channel
        await self.channel_layer.group_add(self.name, self.channel_name)

        # accept the connection
        await self.accept()
        print(f'[{self.name}] You are connected to the channel {self.channel_name}')

    async def websocket_receive(self, event):
        print(f'[{self.name}] Received message {event["text"]}')
