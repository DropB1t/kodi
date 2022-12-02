from services.people import peopleRecognition as PR
from services.emotions import emotionRecognition as ER
from services.advices import consigli as AD
import random

cl1 = ER.begin()
cl2 = PR.begin()
cl3 = AD.begin_location()
cl4 = AD.begin_song()

count = 0
prevEmt = "buffering"
curEmt = "buffering"
while(True): #amo le attese attive
    if count == 10:#da cambiare sulla macchina finale
        count = 0
        curEmt = ER.getEmotion()
        print("eccomi",curEmt, prevEmt)
        if prevEmt != curEmt:
            print("eccomi")
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
