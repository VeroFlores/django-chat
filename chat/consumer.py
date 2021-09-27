# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

from .models import NegotiationsMessages

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("CONNECTED")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        print("DISCONNECTED")
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("RECEIVED",text_data)
        text_data_json = json.loads(text_data)
        
        message = text_data_json['message']
        date = text_data_json['date']
        user = text_data_json['user']

        NegotiationsMessages.objects.using('whipay').create(message=message, owner_id=int(user))
        
        print("MESSAGE",message)
        
        data = {
            'type': 'chat_message',
            'message': message,
            'date': date,
            'user': user,
        }
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, data    
        )

    # Receive message from room group
    def operacion(self, event):
        print("OPERACION")
        # Send message to WebSocket
        self.send(text_data="Hola desde Whipay")

    # Receive message from room group
    def chat_message(self, event):
        print("MESSAGE")
        data = {
            'date': timezone.now().strftime("%d/%m/%YT%H:%M:%sZ"),
            'server_message': event['message'],
            'user':event['user'],
            'date':event['date']
        }
        print('getMessage',data)
        # Send message to WebSocket
        self.send(text_data=json.dumps(data))