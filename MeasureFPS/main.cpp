#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <time.h>

#define DEBUG 1

using namespace cv;
using namespace std;

int main() {
    VideoCapture cap(0);  // open the default camera
    if (!cap.isOpened())  // check if we succeeded
        return -1;
    namedWindow("Camera Feed");

    // Track time elapsed for computing FPS
    time_t startTime, curTime;

    time(&startTime);
    int numFramesCaptured = 0;
    double secElapsed;
    double curFPS;
    double averageFPS = 0.0;

    while (true) {
        // Get the current frame
        Mat frame;
        cap >> frame;
        // Show the frame
        imshow("Camera Feed", frame);

        numFramesCaptured++;
        // Get the current time and show FPS
        time(&curTime);
        double secElapsed = difftime(curTime, startTime);
        double curFPS = numFramesCaptured / secElapsed;

        cout << "FPS = " << curFPS << endl;
        # if DEBUG
        cout << "secElapsed = " << secElapsed << " secs, numFramesCaptured = " << numFramesCaptured << endl;
        #endif
        // compute running average of frames
        if (secElapsed > 0)
            averageFPS = (averageFPS * (numFramesCaptured - 1) + curFPS)
                                / numFramesCaptured;
        if (waitKey(33) == 27)
            break;
    }

    cout << "Average FPS = " << averageFPS << endl;

    // the camera will be deninitialized automatically in
    // VideoCapture destructor;
    return 0;
}
