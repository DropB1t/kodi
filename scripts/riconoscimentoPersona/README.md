## imgPublishing.py
E' lo script che manda la foto da analizzare. Puo' essere preso come spunto
per creare il client sulla raspberry
**NOTA** le immagini sono encodate usando:
```
img_encode = cv2.imencode('.jpg', img)[1]
data_encode = np.array(img_encode)
byte_encode = data_encode.tobytes()
```
Probabilmente si dovra' trovare un encoding compatibile.
l'input e' preso in
```
img = cv2.imread("./1.jpg")
```
### topic
+ net pensato come top level
+ 0000 e' l'id della macchina
+ camera -> webcam
+ smartwatch (o forse no)

per le risposte stesso id e poi
+ cameraReply
+ smartwatchReply

## imgElaborator.py
vuole le immagini encodate come sopra e restituisce il nome detectato

## Note
A volte la 1.jpg non viene mandata, non so se perche' sbagliavo qualcosa io se 
proprio va spezzettata
