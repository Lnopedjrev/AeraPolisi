from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

import json

from shop.models import Products
from .models import Chats, Messages
from logapp.models import User


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data, chat):
        old_messages = chat.get_last_10()
        content = {
            "type": "fetched",
            "messages": self.messages_to_json(old_messages),
        }
        self.send_message(content)

    def new_message(self, data, chat):
        author = data["author"]
        author_user = User.objects.get(username=author)

        product = None
        if data["product_id"]:
            product = Products.objects.get(id=data["product_id"])

        message_content = data["message"]

        message = Messages.objects.create(
            content=message_content, author=author_user, chat=chat, product=product
        )

        content = {
            "type": "send_message",
            "message": self.message_to_json(message),
        }

        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        message_sended = "{:d}:{:02d}".format(
            message.created.hour, message.created.minute
        )

        return {
            "author": message.author.username,
            "content": message.content,
            "sended": message_sended,
            "product_fc": self.product_to_json(message.product),
        }

    def product_to_json(self, product):
        if product is not None:
            product_ob = {
                "name": product.name,
                "price": product.price,
                "product_url": product.get_absolute_url(),
                "product_image": product.get_first_image(),
            }
            return product_ob
        else:
            return "nothing"

    def connect(self):
        scope = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = str(scope)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        new_command = text_data_json["command"]
        chat = Chats.objects.get(name=self.room_group_name + "_chat")

        if new_command == "new_message":
            self.new_message(text_data_json, chat)
        elif new_command == "fetch_messages":
            self.fetch_messages(text_data_json, chat)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": message["type"],
                "message": message["message"],
            },
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))
