# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("CONNETED")
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
        print("RECEIVED")
        
        data = {
            'type': 'chat_message',
            'message': 'Recibí',
        }
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, data    
        )

    # Receive message from room group
    def operacion(self, event):
        
        # Send message to WebSocket
        self.send(text_data="Hola desde Whipay")

    # Receive message from room group
    def chat_message(self, event):
        data = {
            'date': timezone.now().strftime("%d/%m/%YT%H:%M:%sZ"),
            'server_message': event['message'], 
        }
        # Send message to WebSocket
        self.send(text_data=json.dumps(data))