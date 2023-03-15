import cv2
import os
import sys
import progressbar


def writeFramesFromVideo():

    # ------- Frames Save Path and Make Directory -------#
    savePath = os.path.join(os.getcwd(),sys.argv[2])
    os.makedirs(savePath)

    # ------- Open a Video -------#
    vid = cv2.VideoCapture(sys.argv[1])


    #------- Progress Bar Stuff -------#
    variable = int(sys.argv[4])
    total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))+1

    widgets = [' [',
               progressbar.Timer(format='elapsed time: %(elapsed)s'),
               '] ',
               progressbar.Bar('*'), ' (',
               progressbar.ETA(), ') ',
               ]

    bar = progressbar.ProgressBar(min_value= variable , max_value=total+variable,
                                  widgets=widgets).start()
    #----------------------------------#


    ret = True
    while (ret):
        ret, frame = vid.read()
        if(ret == True and variable % 30 == 0):
            cv2.imwrite(os.path.join(savePath,"{}{}.jpg".format(sys.argv[3],variable)),frame);
        variable+=1
        bar.update(variable)

    vid.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    if (len(sys.argv)== 1):
        print("python3 prepareDatasetFromVideo.py 1.mp4 SoldierFrames soldier 0")
    else :
        writeFramesFromVideo()
