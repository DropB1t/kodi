from threading import Thread
import numpy as np
import base64
import cv2

''' Threaded Class to implement Video Stream '''
class WebcamVideoStream:

    def __init__(self, src=-1):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start() # start the thread to read frames from the video stream
        return self

    def update(self):
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read() #read the next frame from the stream

    def read(self):
        return self.frame # return the frame most recently read

    def stop(self):
        self.stopped = True


''' Class for managing Webcam Stream'''
class VideoCamera:

    def __init__(self):
        self.cap = WebcamVideoStream(src=0).start()


    def get_frame(self):
        image = self.cap.read()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
        blurred = False

        if fm < 300: # Treshhold under which the image proccessed is percepted as blurry
            blurred = True

        ret, jpeg = cv2.imencode('.jpg', image)
        data = np.array(jpeg)
        encoded_text = base64.b64encode(jpeg)
        return encoded_text, data.tobytes(), blurred
