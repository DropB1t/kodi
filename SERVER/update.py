import paho.mqtt.client as mqtt
from services.training import modelGenerator as MG
from services.training import trainer as TR
from services.training import imgRetriever as IR
import re
import shutil as SH

broker = "127.0.0.1"
port = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("update/+")

def on_message(client, userdata, msg):
    car = re.search("/(\d+$)",msg.topic).group(1)
    # TODO update del modello
    MG.generate()
    SH.copy("./services/training/model.json","./services/people/model.json")
    IR.retrieve(car)#TODO va testato
    TR.train()
    SH.copy("./services/training/model_weights.h5", "./services/people/model_weights.h5")
    SH.rmtree("./services/tmp/") #TODO test
    # TODO stop and restart thread





def begin():
    client = mqtt.Client("recognizer")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("127.0.0.1", 1883)
    
    client.loop_forever()
