from services.people import peopleRecognition as PR
from services.emotions import emotionRecognition as ER
from services.advices import consigli as AD
import random
import os

broker = os.getenv('MOSQUITTO_IP')
port = os.getenv('MOSQUITTO_PORT')
user = os.getenv('MONGO_USER')
passw = os.getenv('MONGO_PASSWD')
host = os.getenv('MONGO_IP')
mongoPort = os.getenv('MONGO_PORT')

ER.mqttParams(broker, port)
PR.mqttParams(broker, port)
AD.mqttParams(broker, port)

PR.mongoParams(host, mongoPort, user, passw)
AD.mongoParams(host,mongoPort, user, passw)


cl1 = ER.begin()
cl2 = PR.begin()
cl3 = AD.begin_location()
cl4 = AD.begin_song()

count = 0
prevEmt = "buffering"
curEmt = "buffering"
firstTime = True
while(True): #amo le attese attive
    if count == 10:#da cambiare sulla macchina finale
        count = 0
        curEmt = ER.getEmotion()
        if prevEmt != curEmt:
            if firstTime:
                AD.send_locations_suggestion(curEmt)
                AD.send_songs_suggestion(curEmt)
                firstTime = False
            else:
                if random.randint(0,10) < 2 :
                    AD.send_locations_suggestion(curEmt)
                else:
                    AD.send_songs_suggestion(curEmt)
    ER.giro(cl1)
    PR.giro(cl2)
    AD.giro(cl3)
    AD.giro(cl4)
    prevEmt = curEmt
    count+=1
