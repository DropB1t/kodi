from services.people import peopleRecognition as PR
from services.emotions import emotionRecognition as ER

cl1 = ER.begin()
cl2 = PR.begin()
while(True): #amo le attese attive
    ER.giro(cl1)
    PR.giro(cl2)
