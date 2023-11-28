# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-222
"""
Created on Fri Oct 27 18:17:08 2023

@author: hjr & Nizar........6666666........................
"""

import cv2 # importing cv2 liberary

cam = cv2.VideoCapture(0)

count = 0

while True:
    ret, img = cam.read()

    cv2.imshow("Test", img)

    if not ret:
        break

    k=cv2.waitKey(1)

    if k%256==27:
        #For Esc key
        print("Close")
        break
    elif k%256==32:
        #For Space key
        
        print("Image "+str(count)+"saved")
        file='F:/Images/img'+str(count)+'.jpg'
        cv2.imwrite(file, img)
        count +=1

cam.release
cv2.destroyAllWindows