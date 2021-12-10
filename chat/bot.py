from channels.generic.websocket import AsyncConsumer, AsyncWebsocketConsumer
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import comparisons

import uuid


class BotConsumer(AsyncWebsocketConsumer):

    def __init__(self):
        self.bot = ""
        self.message = ""
        self.name = ""
        self.chatbot = None

    async def websocket_connect(self, event):
        self.name = self.scope["url_route"]["kwargs"]["name"]
        # add user into channel
        await self.channel_layer.group_add(self.name, self.channel_name)

        # Create a new chat bot named Charlie
        self.chatbot = ChatBot(self.name, logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "statement_comparison_function": comparisons.LevenshteinDistance,
            }
        ])
        trainer = ChatterBotCorpusTrainer(self.chatbot)

        trainer.train(
            "chatterbot.corpus.english.greetings",
            "chatterbot.corpus.english.conversations"
        )

        # accept the connection
        await self.accept()
        print(f'[{self.name}] You are connected to the channel {self.channel_name}')

    async def websocket_receive(self, event):
        self.message = event['text']
        print(f'[{self.name}] Received message {self.message}')

        response = self.chatbot.get_response(self.message)

        response = response.serialize()
        self.bot = response['text']

        await self.channel_layer.group_send(self.name, {
            "type": "send.message",
            "text": response['text'],
        })

    async def send_message(self, event):
        bot_id = str(uuid.uuid4())
        message_id = str(uuid.uuid4())
        response = json.dumps({
            'bot': {
                "id": bot_id,
                "text": self.bot
            },
            'message': {
                "id": message_id,
                "text": self.message
            }
        })
        await self.send(response)
