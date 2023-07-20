
#%matplotlib inline
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame2 = cap.read()
    key = cv2.waitKey(1)
    if key == 27:
        break


    #img = cv2.imread('bolinha.png')

    img_rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)


    # Definição dos valores minimo e max da mascara
    # o magenta tem h=300 mais ou menos ou 150 para a OpenCV
    image_lower_hsv = np.array([140, 50, 100])  
    image_upper_hsv = np.array([170, 255, 255])


    mask_hsv = cv2.inRange(img_hsv, image_lower_hsv, image_upper_hsv)

 
    cv2.imshow('test', mask_hsv)
    #cv2.imshow("Eye of the robot", frame2)
