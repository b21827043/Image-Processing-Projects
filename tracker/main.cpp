#include <opencv2/core/utility.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/tracking.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/tracking/tracking_legacy.hpp>
#include <iostream>
#include <cstring>
#include <cmath>
using namespace std;
using namespace cv;
int main(){
  chrono::steady_clock::time_point Tbegin, Tend;
  float f;
  float FPS[16];
  int i, Fcnt=0;
  int fpsvid;
  // declares all required variables
  Rect roi;
  Mat frame;
  // create a tracker object
  Ptr<Tracker> tracker = TrackerCSRT::create();
  // set input video

  VideoCapture cap(0);
  // get bounding box
  cap >> frame;
  fpsvid = cap.get(CAP_PROP_FPS);
  cout<<fpsvid;
  roi=selectROI("tracker",frame);
  //quit if ROI was not selected
  if(roi.width==0 || roi.height==0)
    return 0;
  // initialize the tracker
  tracker->init(frame,roi);
  // perform the tracking process
  printf("Start the tracking process, press ESC to quit.\n");
  for ( ;; ){
    Tbegin = chrono::steady_clock::now();	
    // get frame from the video
    cap >> frame;
    // stop the program if no more images
    
    if(frame.rows==0 || frame.cols==0)
      break;
    // update the tracking result
    tracker->update(frame,roi);
    // draw the tracked object
    rectangle( frame, roi, Scalar( 255, 0, 0 ), 2, 1 );
    
    Tend = chrono::steady_clock::now();

    f = chrono::duration_cast <chrono::milliseconds> (Tend - Tbegin).count();
    if(f>0.0) FPS[((Fcnt++)&0x0F)]=1000.0/f;
    for(f=0.0, i=0;i<16;i++){ f+=FPS[i]; }
    putText(frame, format("FPS %0.2f", f/16),Point(10,20),FONT_HERSHEY_SIMPLEX,0.6, Scalar(0, 0, 255));

    // show image with the tracked object
    imshow("tracker",frame);
    //quit on ESC button
    if(waitKey(1)==27)break;
  }
  return 0;
}
