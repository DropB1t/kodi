import threading
import time
import cv2
import base64

class Camera:
    def __init__(self):
        self.thread = None
        self.current_frame  = None
        self.is_running: bool = False
        self.pause: float = 0.015
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("Could not open video device")
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def __del__(self):
        self.camera.release()

    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self._capture)
            self.thread.start()

    def get_frame(self):
        return self.current_frame

    def set_pause(self,num: float = 0.015):
        self.pause = num

    def stop(self):
        self.is_running = False
        if self.thread is not None:
            self.thread.join()
        self.thread = None

    def _capture(self):
        try:
            self.is_running = True
            while self.is_running:
                time.sleep(self.pause)
                ret, frame = self.camera.read()
                #print('Frame fetched')
                if ret:
                    ret, encoded = cv2.imencode(".jpg", frame)
                    if ret:
                        self.current_frame = base64.b64encode(encoded)
                    else:
                        print("Failed to encode frame")
                else:
                    print("Failed to capture frame")
        except KeyboardInterrupt:
            print("Video Stream Interrupted")

        print("Reading thread stopped")
        self.thread = None
        self.is_running = False
