import json
import time
import datetime

from channels.generic.websocket import WebsocketConsumer


class TestConsumer(WebsocketConsumer):
    def connect(self,*args,**kwargs):
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def receive(self, text_data=None, bytes_data=None):
        self.send(f'{str(datetime.datetime.now())}zoba karolina, dziala')

    def send_user(self, event):

        self.send(json.dumps({"ping": "pong"}))