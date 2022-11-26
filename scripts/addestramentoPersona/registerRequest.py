import paho.mqtt.client as mqtt
import cv2
import numpy as np

broker="127.0.0.1"
port=1883


def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
client1= mqtt.Client("testPubisherForTraining")                           #create client object
client1.on_publish = on_publish                         #assign function to callback
client1.on_connect = on_connect
client1.connect(broker,port)                                 #establish connection


client1.publish("register/0000",person)

