from pymongo import MongoClient
import cv2
import numpy as np
def get_database():

   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://root:root@localhost:27017/"

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   # Create the database for our example (we will use the same database throughout the tutorial
   return client['test']

# Get the database
dbname = get_database() 

img = cv2.imread("./1.png")
img_encode = cv2.imencode('.png', img)[1]
data_encode = np.array(img_encode)
byte_encode = data_encode.tobytes()

collection_name = dbname["0000"]
foto1 = {
        "user_id" : 0,
        "nome" : "Mario",
        "cognome" : "Rossi",
        "foto_id" : 0,
        "foto" : byte_encode
}

collection_name.insert_one(foto1)
