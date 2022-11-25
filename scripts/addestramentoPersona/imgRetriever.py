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

collection_name = dbname["0000/1"]

item_details = collection_name.find()

for item in item_details:
    print(item['nome'])
    imag = np.frombuffer(item['foto'], dtype=np.uint8)
    img = cv2.imdecode(imag, cv2.IMREAD_COLOR)
    #cv2.imwrite('./retrieved.png',img)

