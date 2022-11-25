import paho.mqtt.client as mqtt
import cv2
import numpy as np
import os

broker="127.0.0.1"
port=1883
#img = cv2.imread("./1.jpg")
#img_encode = cv2.imencode('.jpg', img)[1]
#data_encode = np.array(img_encode)
#byte_encode = data_encode.tobytes()

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
client1= mqtt.Client("testPubisherForTraining")                           #create client object
client1.on_publish = on_publish                         #assign function to callback
client1.on_connect = on_connect
client1.connect(broker,port)                                 #establish connection
#ret= client1.publish("training/0000/0",byte_encode)                   #publish
dir = os.listdir('./img')
for imgName in dir:
    imgPath = './img/'+imgName;
    img = cv2.imread(imgPath)
    img_encode = cv2.imencode('.jpg', img)[1]
    data_encode = np.array(img_encode)
    byte_encode = data_encode.tobytes()
    client1.publish("training/0000/0",byte_encode)

