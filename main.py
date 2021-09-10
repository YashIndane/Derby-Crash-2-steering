"""
You just have to use whitescreen of your phone , and hold the screen towards the webcam. 
Now just steer your phone to drive or race a vehical in a game.
"""

import cv2
import time
import pyautogui

time.sleep(5)

pyautogui.FAILSAFE = True
cap = cv2.VideoCapture(0)

# This parameters can be changed accordingly
frame_counter = 0
FRAME_ADJUST = 5
SENSITIVITY = 0.25
SPEED = 20
TIME_OF_ACTION = 0.3
AREA_COMPARE = 6000

while True : 

    if frame_counter % FRAME_ADJUST == 0 : pyautogui.press("up", presses = SPEED)

    success, img_org = cap.read()
    img = cv2.cvtColor(img_org, cv2.COLOR_BGR2GRAY)

    _, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY) 
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    for cnt in contours : 
        
        area = cv2.contourArea(cnt) 
    
        # Capturing grid squares by area 
        if area > AREA_COMPARE : 

            approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True) 
    
            # Only grabbing 4 sided polygons
            if len(approx) == 4 :  
                   
                x, y, w, h = cv2.boundingRect(cnt)  
                    
                n = approx.ravel()  
                i = 0
                coordinates = []

                for j in n : 

                    if i % 2 == 0 : 

                        x_c = n[i] 
                        y_c = n[i + 1] 

                        coordinates.append([x_c, y_c]) 

                    i += 1 

                coordinates = sorted(coordinates, key = lambda x : x[0])

                P1 = coordinates[:2]
                P2 = coordinates[2:]

                P1 = sorted(P1, key = lambda z : z[1])
                P2 = sorted(P2, key = lambda q : q[1])

            try : 

                # This block of code makes the game movements
                x2, y2 = P2[0]
                x1, y1 = P1[0]

                # Calculating slope of edge of the rectangle
                slope = (y2 - y1)/(x2 - x1)
                print(slope)

                if slope >= SENSITIVITY :

                    pyautogui.keyDown("left")
                    time.sleep(TIME_OF_ACTION)
                    pyautogui.keyUp("left")

                elif slope <= -SENSITIVITY :

                    pyautogui.keyDown("right")
                    time.sleep(TIME_OF_ACTION)
                    pyautogui.keyUp("right")

            except : pass    

    frame_counter += 1

    if cv2.waitKey(1) & 0xFF == ord("q") : break
