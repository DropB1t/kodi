from tensorflow.keras.models import model_from_json
import numpy as np

import cv2
import tensorflow as tf
import numpy as np
import sys
import paho.mqtt.client as mqtt



class PersonModel(object):

    PERSONS_LIST = ["Antonio Bruni","Davide Bruni",
                    "Davide Tonellotto"]

    def __init__(self, model_json_file, model_weights_file):
        # load model from JSON file
        with open(model_json_file, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)

        # load weights into the new model
        self.loaded_model.load_weights(model_weights_file)
        self.loaded_model.make_predict_function()

    def predict_person(self, img):
        self.preds = self.loaded_model.predict(img)
        return PersonModel.PERSONS_LIST[np.argmax(self.preds)]

facec = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = PersonModel("./model.json", "./model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        self.img = cv2.imread("./1.jpg") #TODO prendilo da rabbit
    def get_frame(self):
        fr = self.img
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)
        index = np.where(faces == np.max(faces,axis=0)[2])[0][0]
        #esempio di faces
        #[[  34 1280  104  104]
        # [ 327  442  761  761]]
        #np.max prende il massimo per ogni colonna
        #una riga di questa matrice e' composta come (x, y, width, height) e con [2] prendo width
        #where trova le coordinate del massimo valore di width
        #where restituisce due array il primo delle colonne in cui fa match e il secondo delle righe
        # con [0][0] prendo il primo valore del primo array
        # Questo lo faccio per prendere la faccia piu' grande e quindi piu' vicina alla telecamera che
        # si suppone sia il guidatore
        x, y, w, h = faces[index]
        fc = gray_fr[y:y+h, x:x+w]
        roi = cv2.resize(fc, (48, 48))
        pred = model.predict_person(roi[np.newaxis, :, :, np.newaxis])
            #print(pred)
            #broker = "127.0.0.1"
            #port = 1883
            #client = mqtt.Client("contol1")
            #client.on_publish = self.on_publish
            #client.connect(broker,port)
            #ret = client.publish("macchina",pred)
        print(pred)
        return fr
    def on_publish(self,client, userdata, result):
        print("data published\n")
        pass
test = VideoCamera()
test.get_frame()
