from pymongo import MongoClient
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import re

broker = "127.0.0.1"
port = 1883

def get_database():

   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://root:root@localhost:27017/"

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   # Create the database for our example (we will use the same database throughout the tutorial
   return client['trainingDatabase']

def store(car, uid, img):
    dbname = get_database()
    collection_name = dbname[car][uid]
    sizeT = list(collection_name.find())
    startingId = 0
    if len(sizeT) != 0:
        startingId = list(collection_name.find().sort("foto_id",-1).limit(1))[0]["foto_id"]
    foto = {
            "foto_id" : startingId+1,
            "foto" : img
    }
    collection_name.insert_one(foto)#TODO cambia con insert_many

def on_connect(client, userdata, flags, rc):

    client.subscribe("training/+/+")

def on_message(client, userdata, msg):
    car = re.search('/(.*0)/',msg.topic).group(1)
    uid = re.search("/(\d+$)",msg.topic).group(1)
    store(car, uid, msg.payload)

def begin():
    client = mqtt.Client("storer")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    client.loop_forever()
