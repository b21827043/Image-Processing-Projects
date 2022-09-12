from threading import Thread
import cv2
from datetime import datetime

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        self.status=0
        self.first_frame=None
        self.status_list=[None,None]
        self.times=[]

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:

                (self.grabbed, self.frame) = self.stream.read()

                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)

                if self.first_frame is None:
                    self.first_frame = gray
                    continue

                delta_frame = cv2.absdiff(self.first_frame, gray)
                thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
                thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

                (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in cnts:
                    if cv2.contourArea(contour) < 10000:
                        continue
                    self.status = 1

                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                self.status_list.append(self.status)

                self.status_list = self.status_list[-2:]

                if self.status_list[-1] == 1 and self.status_list[-2] == 0:
                    self.times.append(datetime.now())
                if self.status_list[-1] == 0 and self.status_list[-2] == 1:
                    self.times.append(datetime.now())

    def stop(self):
        self.stopped = True
