from threading import Thread
from services.people import peopleRecognition as PR
from services.emotions import emotionRecognition as ER
#from services.training import imgStorer as IS
#from services.training import personRegisterer as RE
#import update as UP

#th1 = Thread(target = PR.begin())
th2 = Thread(target = ER.begin())
#th3 = Thread(target = IS.begin())
#th4 = Thread(target = RE.begin())
#th5 = Thread(target = UP.begin())

#th1.start()
th2.start()
#th3.start()
#th4.start()
#th5.start()

#non so quando chiamare il training
#ricevo richiesta di registrazione
#faccio partire il training
#aggiorno gli altri script
