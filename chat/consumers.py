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

from gtts import gTTS
            # 0import os

#for email
import smtplib, ssl
import re


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
        # feedback = learning2.feedback(message)
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
            reply = learning2.response(message)
            possible_query = learning2.poss_query(message)
            result = learning2.email_intent(message)
            print(result[0])

        
               
            # tts = gTTS(text=reply, lang='en')
            # tts.save("reply.mp3")
            # # os.system("good.mp3")
            # os.system("mpg321 reply.mp3 -quiet")

            link = learning2.open_link(message)



            

            port = 465  # For SSL
            smtp_server = "smtp.gmail.com"
            sender_email = "nitesh.ghimire@gmail.com"  # Enter your address
            password = "mithrandir"


            if result[0]=="email_user":
                line = message
                match = re.search(r'[\w\.-]+@[\w\.-]+', line)
                # print(match)
                try:
                    email = match.group(0)
                    print(email)
                    receiver_email = email  # Enter receiver address
                    mess = """\
                    Ashley's Info

                    Please visit http://www.ashleyberges.com/contact-us/ to sbscribe"""
                   
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, mess)
                except:
                    reply = "Please give your correct email adress."
                    print("Email not in the line")




            # receiver_email = email  # Enter receiver address
            # mess = """\
            #     Subject: Hi there

            #     This message is sent from Python."""

            # context = ssl.create_default_context()
            # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            #     server.login(sender_email, password)
            #     server.sendmail(sender_email, receiver_email, message)

            
            tags = possible_query

            value=""
            pos_value ="Positive"
            neg_value ="Negetive"

            # pf = open('chat/chatModel/feedback.txt', 'a')
            # if value==pos_value:
            #     feedback = pf.write("\n\n" + "Query:" + message + "\n" + "Reply:" + reply + "\n" + "Feedback:" + pos_value)
            # elif value==neg_value:
            #     feedback = pf.write("\n\n" + "Query:" + message + "\n" + "Reply:" + reply + "\n" + "Feedback:" + neg_value)
            # else:
            #     feedback = pf.write("\n\n" + "Query:" + message + "\n" + "Reply:" + reply + "\n" + "Feedback:" + None)



                
            



    





            # value = ""

            # if value=="positive":
            #     feedback = learning2.pos_feedback(message)
            # elif value=="negetive":
            #     feedback = learning2.neg_feedback(message)
            # else:
            #     pass

            # print("pF",pos_feedback)
            # print("nF",neg_feedback)

            # tagss = response.tags
            
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
            'link': link,
            'tags':tags,
            'value':value,
            # 'feedback':feedback,
            # 'neg_feedback':neg_feedback
            # 'feedback':feedback,
        }))




