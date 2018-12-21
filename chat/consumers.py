# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json

import importlib
import random

from chat.chatModel import learning2
#from chat.chatModel.restaurants.learning2 import welcome_msg
from chat.train_mode import check_train_mode,enter_train_mode
import subprocess

from subprocess import Popen
import os
lock=0

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        global lock
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # pos_feedback = learning2.pos_feedback()
        # neg_feedback = learning2.neg_feedback(message)
        # print(neg_feedback)

        # feedback = str(feedback(message))
        train_switch=check_train_mode(message)
        if train_switch== True or lock==1:
            print("training mode enabled")
            rep= (enter_train_mode(message))
            reply = ["<strong style='color:MediumSeaGreen;'>Training in progress...</strong>"]
            #print(rep)
            lock=rep[1]
            #print(lock)
            reply=rep[0]

        elif train_switch==False and lock==0:
            reply = str(learning2.response(message))
            
            #print(reply)

        elif train_switch==3:

            #stop model
            subprocess.check_call(["python3", "./chat/chatModel/model2.py"])
            reply = "<strong>Training in progress...</strong>"
            #modelreload
            importlib.reload(learning2)
            #print(os.system('./chat/chatModel/restaurants/model2.py'))

            reply="Training process finished.<br>Thank you for teaching me &#9757;.<br>Now you can ask me the query you trained me on."

        self.send(text_data=json.dumps({
            'message': message,
            'reply':reply,
            'positive':learning2.pos_feedback(),
            'negetive' : learning2.neg_feedback(message),
            # 'feedback':feedback,
        }))




