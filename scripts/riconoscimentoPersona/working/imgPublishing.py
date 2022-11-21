import paho.mqtt.client as mqtt
import cv2
import numpy as np

broker="127.0.0.1"
port=1883
img = cv2.imread("./2.png")
img_encode = cv2.imencode('.png', img)[1]
data_encode = np.array(img_encode)
byte_encode = data_encode.tobytes()

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass


client1= mqtt.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
#client1.username_pw_set("mqtt-test", "mqtt-test")
client1.connect(broker,port)                                 #establish connection
#ret= client1.publish("camera",byte_encode)                   #publish
ret= client1.publish("net/0000/camera",byte_encode)                   #publish
print(ret)
