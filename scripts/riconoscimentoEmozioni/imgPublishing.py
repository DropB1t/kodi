import paho.mqtt.client as mqtt
import cv2
import numpy as np

broker="127.0.0.1"
port=1883
img = cv2.imread("./1.jpg")
img_encode = cv2.imencode('.jpg', img)[1]
data_encode = np.array(img_encode)
byte_encode = data_encode.tobytes()

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client1.subscribe("emt/0000/cameraReply")
    
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    print(msg.topic)
    print(msg.payload)
    #client1.loop_stop()
    exit(0) # un po' ignorante ma funziona


client1= mqtt.Client("raspberry")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.on_message = on_message
client1.on_connect = on_connect
#client1.username_pw_set("mqtt-test", "mqtt-test")
client1.connect(broker,port)                                 #establish connection
#ret= client1.publish("camera",byte_encode)                   #publish
ret= client1.publish("emt/0000/camera",byte_encode)                   #publish
client1.loop_forever()
