from pymongo import MongoClient
import random
import paho.mqtt.client as mqtt
import json

broker = ""
port = 0
mongoUser = ""
mongoPasswd = ""
mongoHost = ""
mongoPort = ""

def mqttParams(brokerL, portL):
	global broker
	global port
	broker = brokerL
	port = int(portL)

def mongoParams(host, port, user, passw):
    global mongoUser
    global mongoPasswd
    global mongoHost
    global mongoPort
    mongoHost = host
    mongoUser = user
    mongoPasswd = passw
    mongoPort = port

def get_database():
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = f"mongodb://{mongoUser}:{mongoPasswd}@{mongoHost}:27017/"

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   # Create the database for our example (we will use the same database throughout the tutorial
   return client['kodi']


def get_songs_from_emotion(emotion):
    # return the top 2 choice + 1 random choice
    dbname = get_database()
    collection = dbname["0000"]["songs"]
    suggested = []
    top_two = collection.find({},{"_id":0,"name":1,"album":1, "artists":1}, allow_disk_use=True).limit(3)
    random_result = collection.find({},{"_id":0,"name":1,"album":1, "artists":1}, allow_disk_use=True).sort(emotion,-1).skip(random.randint(3,1204025)).limit(2)
    for x in top_two:
        suggested.append(x)
    for x in random_result:
        suggested.append(x)
    return suggested

def get_location_from_emotion(emotion):
    # return the top 2 choice + 1 random choice
    dbname = get_database()
    collection = dbname["0000"]["locations"]
    suggested = []
    top_two = collection.find({},{"_id":0,"name":1,"latitude_radian":1, "longitude_radian":1}, allow_disk_use=True).sort(emotion,-1).limit(3)
    random_result = collection.find({},{"_id":0,"name":1,"latitude_radian":1, "longitude_radian":1}, allow_disk_use=True).sort(emotion,-1).skip(random.randint(3,424205)).limit(2)
    for x in top_two:
        suggested.append(x)
    for x in random_result:
        suggested.append(x)
    return suggested

def update_song(doc, emotion,point): #want a doc (JSON object) with name and album
    dbname = get_database()
    collection = dbname["0000"]["songs"]
    newvalues = {"$inc": {emotion: point}}
    collection.update_one(doc,newvalues)

def update_location(name, emotion,point): #want a JSON (name: name_to_match}
    dbname = get_database()
    collection = dbname["0000"]["locations"]
    newvalues = {"$inc": {emotion: point}}
    collection.update_one(name,newvalues)



def send_locations_suggestion(emotion):
    res = get_location_from_emotion(emotion)
    client = mqtt.Client("emotionSuggester")
    client.connect(broker,port)
    client.publish("adv/0000/placeList",json.dumps(res))

def send_songs_suggestion(emotion):
    res = get_songs_from_emotion(emotion)
    client = mqtt.Client("locationSuggester")
    client.connect(broker,port)
    client.publish("adv/0000/musicList",json.dumps(res))
    
def on_message_song(client, userdata, msg):
    id = re.search('/(.*)/', msg.topic).group(1)
    upj = json.loads(msg.payload)
    update_song(upj['song'],upj['emotion'],upj['score'])

def on_message_location(client, userdata, msg):
    id = re.search('/(.*)/', msg.topic).group(1)
    upj = json.loads(msg.payload)
    update_location(upj['place'],upj['emotion'],upj['score'])

def on_connect_song(client, userdata, flags, rc):
    print("connected song")

def on_connect_location(client, userdata, flags, rc):
    print("connected location")

def begin_song():
    global broker
    global port
    client = mqtt.Client("songsUpdater")
    client.on_message = on_message_song
    client.on_connect = on_connect_song
    client.connect(broker,port)
    client.subscribe("prsn/+/musicRanking")
    return client

def begin_location():
    global broker
    global port
    #print(broker, port, mongoUser, mongoPasswd)
    client = mqtt.Client("locationUpdater")
    client.on_message = on_message_location
    client.on_connect = on_connect_location
    client.connect(broker,port)
    client.subscribe("prsn/+/placeRanking")
    return client

def giro(client):
    client.loop(0.1)

'''
# update_song({'name': 'Testify', 'album': 'The Battle Of Los Angeles'},"Happy",5)
update_location({name:"YAYCHI, WEST AZERBAIJAN"},"Happy",5)
for x in get_location_from_emotion("Happy"):
    print(x)
'''
