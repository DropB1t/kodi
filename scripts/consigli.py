from pymongo import MongoClient
import random
def get_database():

   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://localhost:27017/"

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   # Create the database for our example (we will use the same database throughout the tutorial
   return client['kodi']


def get_songs_from_emotion(emotion):
    # return the top 2 choice + 1 random choice
    dbname = get_database()
    collection = dbname["songs"]
    suggested = []
    top_two = collection.find({},{"_id":0,"name":1,"album":1, "artists":1}).sort(emotion,-1).limit(2)
    random_result = collection.find({},{"_id":0,"name":1,"album":1, "artists":1}).sort(emotion,-1).skip(random.randint(3,1204025)).limit(1)
    for x in top_two:
        suggested.append(x)
    for x in random_result:
        suggested.append(x)
    return suggested

def get_location_from_emotion(emotion):
    # return the top 2 choice + 1 random choice
    dbname = get_database()
    collection = dbname["location"]
    suggested = []
    top_two = collection.find({},{"_id":0,"name":1,"latitude_radian":1, "longitude_radian":1}).sort(emotion,-1).limit(2)
    random_result = collection.find({},{"_id":0,"name":1,"latitude_radian":1, "longitude_radian":1}).sort(emotion,-1).skip(random.randint(3,424205)).limit(1)
    for x in top_two:
        suggested.append(x)
    for x in random_result:
        suggested.append(x)
    return suggested

def update_song(doc, emotion,point): #want a doc (JSON object) with name and album
    dbname = get_database()
    collection = dbname["songs"]
    newvalues = {"$inc": {emotion: point}}
    collection.update_one(doc,newvalues)

def update_location(name, emotion,point): #want a JSON (name: name_to_match}
    dbname = get_database()
    collection = dbname["location"]
    newvalues = {"$inc": {emotion: point}}
    collection.update_one(name,newvalues)

'''
# test
for x in get_location_from_emotion("Happy"):
    print(x)
# update_song({'name': 'Testify', 'album': 'The Battle Of Los Angeles'},"Happy",5)
update_location({name:"YAYCHI, WEST AZERBAIJAN"},"Happy",5)
for x in get_location_from_emotion("Happy"):
    print(x)
'''