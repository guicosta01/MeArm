# ESTA013−17 − NA1 (ou NA2) − 2Q.2023
# EXERCICIO COMPUTACIONAL 02
#
# RA: <seu RA>
# NOME: <seu nome>
#
# E−MAIL: <seu e−mail institucional>
#
# DESCRICAO:
# − Descreva em linhas gerais, o que o seu codigo esta fazendo;
# − Nao esqueca de inserir comentarios pertinentes ao completo
# entendimento do codigo.

import numpy as np
import cv2


cap = cv2.VideoCapture(0)
prevcircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2 + (y1-y2)**2

while True:
    ret, frame = cap.read()

   
    #(esc == 27) for quit
    key = cv2.waitKey(1)
    if key == 27:
        break

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (17,17), 0)

    circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=30, minRadius=75, maxRadius=400)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0,:]:
            if chosen is None: chosen = i
            if prevcircle is not None:
                if dist(chosen[0],chosen[1],prevcircle[0],prevcircle[1]) <= dist(i[0],i[1],prevcircle[0],prevcircle[1]):
                    chosen = i
        cv2.circle(frame, (chosen[0], chosen[1]), 1, (0,100,100), 3)  
        cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (255,0,255), 3)    
        prevcircle = chosen
        cv2.putText(frame, 'Circle', (10,50), 0, 1, (0,255,0),2)
        print(chosen[0])
        print(chosen[1])
        #cv2.putText(frame, str(dist), (10,50), 0, 1, (0,255,0),2)


    if circles is None:
        cv2.putText(frame, 'Square', (10,50), 0, 1, (0,255,0),2)


    #param1 - baixo acha mt circulo
    cv2.imshow("Eye of the robot", frame)

    #show the color on screem
    #cv2.putText(frame, color, (10,50), 0, 1, (0,255,0),2)

    #cv2.imshow("Eye of the robot", frame)


    
    

