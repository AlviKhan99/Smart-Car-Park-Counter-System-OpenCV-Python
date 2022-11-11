#Import all Modules:
import cv2
import pickle
import cvzone
import numpy as np
###

cap = cv2.VideoCapture('carPark.mp4') #Video feed

#Load all the file (f) data into position list:
with open('CarParkPositions', 'rb') as f:
    positionList = pickle.load(f)
###

width, height = 107, 48 #Parking location rectangle width and height

def checkParkingSpace(imgProcessed):
    
    spaceCounter = 0 #Initialize the space counter as 0

    for pos in positionList:
        x, y = pos
        imgCrop = imgProcessed[y:y + height, x:x + width] #Crop all the individual parking spaces.
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop) #Count the number of pixels of the individual parking spaces.
        
        #If count is less than 950; parking spaces are free else parking spaces are not free.
        if count < 950:
            color = (0,255,0)
            thickness = 5
            spaceCounter += 1 #Increment the space counter when the parking spaces are free.
        else:
            color = (0,0,255)
            thickness = 2     
              
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness) #Display all the parking positions within the position list using the rectangle method.
        cvzone.putTextRect(img, str(count), (x, y+height-3), scale=1, thickness=2, offset=0, colorR= color) #Put pixel values beside the imdividual parking spaces.
        cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(positionList)}', (100,50), scale=3, thickness=3, offset=20, colorR=(0,200,0)) #Display number of free parking spaces in the parking zone.

while True:

    # if current frame value is equal to total frame value, set the current frame value to zero. (This loops the video)
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ###
    success, img =  cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Make image gray
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1) #Blur image
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16) #Add image threshold, adaptive threshold in this case.
    imgMedian = cv2.medianBlur(imgThreshold, 5) #Remove the unnecessary noises in the image using median blur.
    kernel = np.ones((3, 3), np.uint8) #Image dilation kernel.
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)#Make the image pixels thicker using image dilation.
 

    checkParkingSpace(imgDilate) #Calling the check parking space function.

    
    cv2.imshow('Image', img)
    cv2.waitKey(10)