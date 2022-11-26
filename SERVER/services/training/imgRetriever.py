from pymongo import MongoClient
import cv2
import numpy as np
import os
def get_database():

   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://root:root@localhost:27017/"

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   # Create the database for our example (we will use the same database throughout the tutorial
   return client['trainingDatabase']

# Get the database
def retrieve(car):
    dbname = get_database() 
    
    collection_name = dbname[car]["people"]
    
    item_details = collection_name.find()
    
    for item in item_details:
        os.mkdir("./services/tmp/train/"+item["person"])
        os.mkdir("./services/tmp/test/"+item["person"])
        cn = dbname[car][item['person_id']]
        photos = list(cn.find())
        dim = len(photos)
        trainDim = round(dim*0.7)
        testDim = dim-trainDim
        for i in range(0,trainDim,1):
            imag = np.frombuffer(photos[i]['foto'], dtype = np.uint8)
            img = cv2.imdecode(imag, cv2.IMREAD_COLOR)
            cv2.imwrite("./services/tmp/train"+item["person"]+"foto"+i+".png",img)
        for i in range(0,testDim,1):
            imag = np.frombuffer(photos[i+trainDim]['foto'], dtype = np.uint8)# TODO da testare
            img = cv2.imdecode(imag, cv2.IMREAD_COLOR)
            cv2.imwrite("./services/tmp/test"+item["person"]+"foto"+i+".png",img)




#retrieve("0000")
