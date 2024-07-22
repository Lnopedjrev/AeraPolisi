from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

import json

from shop.models import Products, ProductOffers
from logapp.models import User


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = str(self.room_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'messsage': 'You are now connected'
        }))

        self.user_customer = User.objects.get(username=self.room_name).customer
        self.user_customer.online_status = True
        self.user_customer.save()

    def disconnect(self, code):
        self.user_customer.online_status = False
        self.user_customer.save()
        self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        offer_id = text_data_json['offer']
        offer = ProductOffers.objects.get(id=offer_id)
        buyer = text_data_json['buyer']
        product = offer.product

        self.room_group_name = str(product.seller.username)

        owner = str(offer.owner.user.username)

        data_to_send = {
                'type': 'chat_message',
                'buyer': buyer,
                'name': product.name,
                'price': product.price,
                'quantity': offer.availability,
                'image_url': product.get_first_image(),
            }

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            data_to_send
        )

        if owner != self.room_group_name:
            async_to_sync(self.channel_layer.group_send)(
                owner,
                data_to_send
            )

    def chat_message(self, event):
        buyer = event['buyer']
        name = event['name']
        price = event['price']
        quantity = event['quantity']

        self.send(text_data=json.dumps({
            'type': 'notification',
            'buyer': buyer,
            'name': name,
            'price': price,
            'quantity': quantity,
            'image': event['image_url'],
        }))
