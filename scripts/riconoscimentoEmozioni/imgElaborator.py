import paho.mqtt.client as mqtt
import cv2
import tensorflow as tf
from tensorflow.keras.models import model_from_json
import numpy as np
import sys
import re

broker = "127.0.0.1"
port = 1883

class FacialExpressionModel(object):

    EMOTIONS_LIST = ["Angry","Disgust",
                    "Fear","Happy",
                    "Neutral","Sad",
                    "Surprise"]

    def __init__(self, model_json_file, model_weights_file):
        # load model from JSON file
        with open(model_json_file, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)

        # load weights into the new model
        self.loaded_model.load_weights(model_weights_file)
        self.loaded_model.make_predict_function()

    def predict_emotion(self, img):
        self.preds = self.loaded_model.predict(img)
        return FacialExpressionModel.EMOTIONS_LIST[np.argmax(self.preds)]


facec = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = FacialExpressionModel("./model.json", "./model_weights.h5")

def recognize(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = facec.detectMultiScale(gray_image, 1.3, 5)
    if len(faces) == 0:
        return "none"
    index = np.where(faces == np.max(faces,axis=0)[2])[0][0]
    # esempio di faces
    # [[  34 1280  104  104]
    #  [ 327  442  761  761]]
    # np.max prende il massimo per ogni colonna
    # una riga di questa matrice e' composta come (x, y, width, height) e con [2] prendo width
    # where trova le coordinate del massimo valore di width
    # where restituisce due array il primo delle colonne in cui fa match e il secondo delle righe
    # con [0][0] prendo il primo valore del primo array
    # Questo lo faccio per prendere la faccia piu' grande e quindi piu' vicina alla telecamera che
    # si suppone sia il guidatore
    x, y, w, h = faces[index]
    resImg = gray_image[y:y+h, x:x+w]
    roi = cv2.resize(resImg, (48, 48))
    pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
    return pred

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def respond(person,id):
    client1= mqtt.Client("control1")                           #create client object
    client1.on_publish = on_publish                          #assign function to callback
    #client1.username_pw_set("mqtt-test", "mqtt-test")
    client1.connect(broker,port)                                 #establish connection
    ret= client1.publish("net/"+id+"/cameraReply",person)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("net/+/camera")



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    result = re.search('/(.*)/', msg.topic)#prendo l'id con regex
    id = result.group(1)
    imag = np.frombuffer(msg.payload, dtype=np.uint8)
    img = cv2.imdecode(imag, cv2.IMREAD_COLOR)#forse come secondo argomento anche 0 per scala di grigi
    pred = recognize(img)
    respond(pred,id)

client = mqtt.Client("recognizer")
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()





