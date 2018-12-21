import json
flag=0
query=''
response=''
intent=''

def check_train_mode(message):
    if message=='@train':
        return True
    elif message=='@begin_train':
        return 3
    else:
        return False
def enter_train_mode(message):
    global flag
    global query
    global response
    global intent
    global lock
    if flag==0:
        reply=["<strong style='color:Tomato;'>You have entered training mode.</strong><br><br> Please provide me the following information about the data in the specified order:<br>1.<strong style='color:DodgerBlue;'>Query</strong><br>2.<strong style='color:DodgerBlue;'>Reply</strong><br>3.<strong style='color:DodgerBlue;'>Intention of the query</strong><br><br>1.Please provide me the query you want to ask to me",1]
    elif flag==1:
        query=message
        reply=["<strong style='color:SlateBlue;'>{}</strong>: is the query.<br><br> 2.Now provide me its reply".format(message),1]
    elif flag==2:
        response=message
        # print("Response working fine",response)
        reply=["<strong style='color:SlateBlue;'>{}</strong>: is the reply for above query. <br><br>3.Now define intention of the query in one word".format(message),1]

    elif flag==3:
        intent=message

        reply=["<strong style='color:SlateBlue;'>{}</strong>: is the intent. <br><br> Now to train me type <strong style='color:Orange;'>@begin_train</strong><br> Please wait for the training completion message!!".format(message),0]
        write_csv()
    # elif flag>3:
    #      reply=['end:',0]
    if flag<3:
        flag+=1
    else:
        flag=0
    return reply

def write_csv():
    global query
    global response
    global intent
    feeds={}
    entry = {'intent': intent, 'query': [query], 'response': [response]}
    with open('./chat/chatModel/ab.json', mode='r',encoding='UTF-8') as feedsjson:
        feeds=json.load(feedsjson)
    #print((feeds['intents']))
    feeds['intents'].append(entry)
    #print(feeds['intents'])
    with open('./chat/chatModel/ab.json', mode='w', encoding='UTF-8') as feedsjson:
        feedsjson.write(json.dumps(feeds))
    print("data added")

    return 0