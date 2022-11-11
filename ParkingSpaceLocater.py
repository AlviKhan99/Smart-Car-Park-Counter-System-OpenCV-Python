#Import all Modules:
import cv2
import pickle #This module saves the parking space locations and helps to bring all those locations in the main code.
###


width, height = 107, 48 #Parking location rectangle width and height

#If file (f) is not empty, load all the file data into position list else create empty postion list:
try:
    with open('CarParkPositions', 'rb') as f:
        positionList = pickle.load(f)
except:
    positionList = [] #To store all position initial x and y coordinates
#####
    

#Activate the mouse click function:
def mouseClick(events, x, y, flags, params):
    #Append initial x and y rectangle coordinates:
    if events == cv2.EVENT_LBUTTONDOWN:
        positionList.append((x,y))
    #Delete the rectangle:
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(positionList): #Important Note: enumerate acts a counter which gives the iteration number, i.
            x1,y1 = pos
            if x1<x<x1+width and y1<y<y1+height:
                positionList.pop(i) #Delete the specific iteration number (i) from the position list.

    
    with open('CarParkPositions', 'wb') as f:
        pickle.dump(positionList, f) #Save the position list inside the file, f using the pickle object.

        
while True:
    img = cv2.imread('carParkImg.png')
    #cv2.rectangle(img, (50,192), (157,240), (255,0,255), 2) #Initial trial static rectangle
    
    #Create rectangles with the specific position initial coordinates provided by left mouse down click:
    for pos in positionList:
       cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255,0,255), 2) 

    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouseClick) #Set and define the mouse callback function.
    cv2.waitKey(1)