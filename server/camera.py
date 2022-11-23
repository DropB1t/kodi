from threading import Thread
import numpy as np
import cv2

''' Class for using another thread for video streaming to boost performance '''


class WebcamVideoStream:

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


''' Class for reading video stream'''


class VideoCamera(object):

    def get_frame(self):
        cap = WebcamVideoStream(src=0).start()
        image = cap.read()
        """ 
        image=cv2.resize(image,(600,500))
        image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        last_frame = image.copy()
        pic = cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB)
        """
        ret, jpeg = cv2.imencode('.jpg', image)
        img = np.array(jpeg)

        return img.tobytes()
