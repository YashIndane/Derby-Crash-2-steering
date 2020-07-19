import cv2
import time
import pyautogui

time.sleep(5)

pyautogui.FAILSAFE = True
cap = cv2.VideoCapture(0)

frame_counter = 0
frame_adjust = 1
sensitivity = 0.25
SPEED = 15
#can tweak the above values

while True : 


        if frame_counter % frame_adjust == 0 :  pyautogui.press('up' , presses = SPEED)

        success, img_org = cap.read()
        

        img = cv2.cvtColor(img_org , cv2.COLOR_BGR2GRAY)
    
        _ , threshold = cv2.threshold(img, 110 , 255 ,cv2.THRESH_BINARY) 

        contours , _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

        for cnt in contours : 
        
            area = cv2.contourArea(cnt) 
    
            # Capturing grid squares by area 
            if area > 6000 :  
                approx = cv2.approxPolyDP(cnt,   0.03 * cv2.arcLength(cnt, True), True) 
    
                # Only grabbing 4 sided polygons
                if(len(approx) == 4):  
                   

                    x , y , w , h = cv2.boundingRect(cnt)  
                    #cv2.drawContours(img_org, [approx], 0, (0, 0, 255), 2)

                    n = approx.ravel()  
                    i = 0
                    coordinates = []
                    for j in n : 
                        if(i % 2 == 0): 
                           x_c = n[i] 
                           y_c = n[i + 1] 

                           coordinates.append([x_c , y_c]) 


                        i += 1 

                    coordinates = sorted(coordinates , key = lambda x : x[0])
                    P1 = coordinates[:2]
                    P2 = coordinates[2:]

                    P1 = sorted(P1 , key = lambda z : z[1])
                    P2 = sorted(P2 , key = lambda q : q[1])

                          

                try : 
                    x2 , y2 = P2[0]
                    x1 , y1 = P1[0]
                    slope = (y2 - y1)/(x2 - x1)
                    print(slope)

                    if slope >= sensitivity :

                         pyautogui.keyDown('left')
                         time.sleep(0.5)
                         pyautogui.keyUp('left')

                    elif slope <= -sensitivity :

                         pyautogui.keyDown('right')
                         time.sleep(0.5)
                         pyautogui.keyUp('right')



                except : pass    

        frame_counter += 1

        #cv2.imshow("window" , img_org)             
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break