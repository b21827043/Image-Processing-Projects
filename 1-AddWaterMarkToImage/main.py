import numpy as np
import cv2

#This function scales the given image to the given width.
def scale(image,scale_width):
    (image_height,image_width) = image.shape[:2]
    new_height = int(scale_width/image_width*image_height)
    return cv2.resize(image,(scale_width,new_height))

#Read the watermark logo.
watermark = scale(cv2.imread("images/watermark.png",cv2.IMREAD_UNCHANGED),300)
(watermark_height,watermark_width) = watermark.shape[:2]

#Read the image to be watermarked.
image1 = cv2.imread("images/image1.jpg")
(image1_height,image1_width) = image1.shape[:2]
image1 = cv2.cvtColor(image1,cv2.COLOR_BGR2BGRA)

#Create a overlay to combine image and watermark.
overlay = np.zeros((image1_height,image1_width,4),dtype="uint8")
overlay[image1_height-watermark_height:image1_height,0:watermark_width] = watermark

#Combaining overlay and watermark.
cv2.addWeighted(overlay,0.8,image1,1.0,0,image1)


while True:
    filename = 'images/savedImage.jpg'
    cv2.imshow("Image1",image1)
    cv2.imwrite(filename,image1)
    if cv2.waitKey(1) == ord("q"):
        break