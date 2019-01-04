# from neo4jrestclient.client import GraphDatabase
# import json
import sqlite3
from sqlite3 import Error

#
# def populate_dataset(intent,l_item,l_query):
#     conn = sqlite3.connect('tags.db')
#     c = conn.cursor()
#     c.execute('''Create TABLE if not exists tag_data (intent TEXT,tag TEXT,query TEXT)''')
#     for tag,query in zip(l_item,l_query):
#
#         if query!=[]:
#             c.execute("INSERT INTO tag_data  VALUES(?,?,?)", (intent,tag,query))
#         else:
#             print("iam tag",tag)
#             continue
#     conn.commit()
#     conn.close()
#     return 0
#
# def prepare_query(intent):
#     #q = 'match(n:{}) -[r:invokes]->(m) Return n,r,m'.format(intent)
#     q='MATCH (n:{})-[r:invokes]->(m) RETURN n.intent,m.intent'.format(intent)
#     return q
#
# def tag_generate(intent):
#     tags=[]
#     n=0
#
#     db = GraphDatabase("http://localhost:7474", username="neo4j", password="subodh")
#     results = db.query(prepare_query(intent))
#     for r in results:
#         tags.append(r[1])
#     return tags
#
#
#
# def prepare_tags():
#     with open('tnt.json', mode='r',encoding='UTF-8') as feedsjson:
#         feeds=json.load(feedsjson)
#         dictionary_item=feeds["intents"]
#
#         for item in dictionary_item:
#             tags=tag_generate(item["intent"])
#             possible_query=generate_query(tags)
#             print(tags,possible_query)
#
#             populate_dataset(item["intent"],tags,possible_query)
#         return 0
#
# def generate_query(tags):
#     possible_query=[]
#     list_item=[]
#     with open('tnt.json', mode='r',encoding='UTF-8') as feedsjson:
#         feeds=json.load(feedsjson)
#     dictionary_item=feeds["intents"]
#     for item in dictionary_item:
#         list_item.append(item["intent"])
#
#     for tag in tags:
#         for item in dictionary_item:
#             if tag==item["intent"] and tag in list_item:
#                 print("how are you?")
#                 possible_query.append(item["query"][0])
#
#             elif tag not in list_item:
#                 possible_query.append('')
#                 break
#
#
#
#     return possible_query


def generate_possible_query(intent):
    possible_query=[]
    print(intent)
    default_list=['About Ashley','Her Contacts']

    conn = sqlite3.connect('chat/chatModel/tags.db')

    cur = conn.cursor()
    cur.execute("SELECT * FROM tag_data WHERE intent=?", (intent,))

    rows = cur.fetchall()


    for row in rows:
        possible_query.append(row[2])
    print("iam the possible query",possible_query)
    if possible_query==[]:

        print("iam possible_qureey inside")
        return default_list
    else:
        print("iam here man")
        return possible_query


# generate_query(['subodh'])
# generate_query(['her_offer'])
# #prepare_tags()
# import json
# def prepare_tags():
#      with open('tnt.json', mode='r',encoding='UTF-8') as feedsjson:
#          feeds=json.load(feedsjson)
#          dictionary_item=feeds["intents"]
#          print(dictionary_item)
#          for item in dictionary_item:
#              print(item["intent"])

#prepare_tags()


