import sys
import cv2
import os

vidDir = sys.argv[1]
video = cv2.VideoCapture(vidDir)
fps = video.get(cv2.CAP_PROP_FPS)
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
duration = length/fps

if not os.path.exists("./img"):
    os.mkdir("./img")


frames = []

def getFrame(sec):
    print("Elaborazione:",round(sec*100/duration,2),"%")
    video.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = video.read()
    if hasFrames:
        width = image.shape[1]
        #image = cv2.flip(image,0)#flip verticale
        cropped = image[0:width, 0:width] # ricordati che prende il quadrato alto della fotocamera(height[from top], width)
        final = cv2.resize(cropped,(48,48))
        cv2.imwrite("./img/image"+str(count)+".jpg", final)
    return hasFrames

sec = 0
frameRate = 0.3 #0.2, 0.3
count=1
success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)
