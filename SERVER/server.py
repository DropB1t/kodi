from threading import Thread
from services.people import peopleRecognition as PR
from services.emotions import emotionRecognition as ER
from services.training import imgStorer as IS

th1 = Thread(target = PR.begin())
th2 = Thread(target = ER.begin())
th3 = Thread(target = IS.begin())

th1.start()
th2.start()
th3.start()
