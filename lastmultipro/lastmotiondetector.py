
import numpy as np
import cv2
import timeit
import time
import multiprocessing
import sys


font = cv2.FONT_HERSHEY_SIMPLEX
# some colors as a bonus
Yellow = (220, 255, 0)
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)
Pink = (255, 0, 255)
Cyan = (220, 255, 0)
# process flags
PROCESS_READY = (1, 1)
PROCESS_BUSY = (2, 2)
PROCESS_SHUTDOWN = (69, 420)

# MAIN FUNCTION ------------------------------------------------------------------------------
# capture video stream from camera source. 0 refers to first camera,
# or write image location, file name only if the image/video is in the same directory as the .py file


def CameraProcess(pipe):
    cap = cv2.VideoCapture(0)
    while True:
        good_frame, frame = cap.read()
        if not good_frame:  # if I got a bad frame, I shutdown
            print("ERROR: NO FRAME")
            pipe.send(PROCESS_SHUTDOWN)
            break

        msg = pipe.recv()  # checks at what state the algorithm process is at right now (busy or ready)
        if msg == PROCESS_READY:
            pipe.send(frame)
        if msg == PROCESS_BUSY:
            good, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()



def AlgorithmProcess(pipe, mainPipe):

    first_frame=None
    status_list=[None,None]

    while True:
        starttime = timeit.default_timer()


        # receiving the frames
        pipe.send(PROCESS_READY)  # sending that i'm ready to receive a frame
        frame = pipe.recv()  # receiving the frame (MP library blocks (freezes) the code until it receives a frame, bear in mind)
        if frame == PROCESS_SHUTDOWN:  # checks if the Camera Process sent a shutdown request
            mainPipe.send(PROCESS_SHUTDOWN)
            break
        pipe.send(PROCESS_BUSY)  # sending that I'm busy from now on, so the camera process will empty the buffer.

        rows, cols, _ = np.shape(frame)  # reads the size of the frame


        """
        ---------------------------------------------
        >> All your computer vision algorithm here <<
        """

        status=0
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray=cv2.GaussianBlur(gray,(21,21),0)

        if first_frame is None:
            first_frame = gray
            continue

        delta_frame = cv2.absdiff(first_frame, gray)
        thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < 10000:
                continue
            status = 1

            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        status_list.append(status)

        status_list = status_list[-2:]


        cv2.imshow("Gray Frame", gray)
        cv2.imshow("Delta Frame", delta_frame)
        cv2.imshow("Threshold Frame", thresh_frame)
        cv2.imshow("Color Frame", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break




        timeend = timeit.default_timer()
        timepass = (int((timeend - starttime) * 1000)) / 1000
        # print all this very interesting stuff
        cv2.putText(frame, "RunTime: {}s".format(timepass), (int(rows * 0.025), int(cols * 0.025)), font, 0.5, Green,
                    1, cv2.LINE_AA)
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # press ESC to exit
            mainPipe.send(PROCESS_SHUTDOWN)
            print("Algorithm Processor: EXIT REQUEST")


if __name__ == "__main__":
    AlgorithmSide, CameraSide = multiprocessing.Pipe()  # creates two sided pipe from algorithm to camera
    MainSide, AlgorithmToMainSide = multiprocessing.Pipe()  # creates a two sided pipe from main to algorithm
    p1 = multiprocessing.Process(target=CameraProcess, args=(AlgorithmSide,))  # creates the camera process
    p2 = multiprocessing.Process(target=AlgorithmProcess, args=(CameraSide, AlgorithmToMainSide))  # creates the algorithm process
    p1.start()  # obviously..
    p2.start()
    while True:  # loops main process to see if i'm ready to shutdown
        if MainSide.recv() == PROCESS_SHUTDOWN:
            print("Main Process: EXIT REQUEST")
            break
    p1.terminate()  # obviously
    print("Camera Process Terminated")
    p2.terminate()
    print("Algorithm Process Terminated")