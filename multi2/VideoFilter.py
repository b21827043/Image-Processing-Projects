from threading import Thread
import cv2,time
from datetime import datetime

class VideoFilter:


    def __init__(self, grabbed=None,frame=None):
        self.grabbed = grabbed
        self.frame = frame
        self.stopped = False

        self.status=0
        self.first_frame=None
        self.status_list=[None,None]
        self.times=[]
        self.prev_frame_time=0
        self.new_frame_time=0

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:

                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)

                # font which we will be using to display FPS
                font = cv2.FONT_HERSHEY_SIMPLEX
                # time when we finish processing for this frame
                self.new_frame_time = time.time()

                # Calculating the fps

                # fps will be number of frame processed in given time frame
                # since their will be most of time error of 0.001 second
                # we will be subtracting it to get more accurate result
                fps = 1 / (self.new_frame_time - self.prev_frame_time)
                self.prev_frame_time = self.new_frame_time

                if self.first_frame is None:
                    self.first_frame = gray
                    continue

                delta_frame = cv2.absdiff(self.first_frame, gray)
                thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
                thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

                (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # converting the fps into integer
                fps = int(fps)

                # converting the fps to string so that we can display it on frame
                # by using putText function
                fps = str(fps)

                # putting the FPS count on the frame
                cv2.putText(gray, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

                print(fps)
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
