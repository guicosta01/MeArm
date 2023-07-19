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
color = ''

while True:
    ret, frame = cap.read()

    #cv2.imshow("Eye of the robot", frame)
    
    #(esc == 27) for quit
    key = cv2.waitKey(1)
    if key == 27:
        break

    #capturar cor apenas dentro de um retangulo     
    height,width,_ = frame.shape
    offset = 150
    campo = frame[offset:height-offset,offset:width-offset]
    #show rec 
    cv2.rectangle(frame,(offset,offset),(width-offset,height-offset),(255,0,0),3)

    corMediaLinha = np.average(campo,axis=0)

    corMedia = np.average(corMediaLinha,axis=0)

    r,g,b = int(corMedia[2]),int(corMedia[1]),int(corMedia[0])

    cor = [r,g,b]
    print(cor)

    # if r >=140 and g>=140 and b <=60:
    #     color = 'Amarelo'
        
    if np.argmax(cor) ==0:
        color = 'Vermelho'

    elif np.argmax(cor) ==1:
        color = 'Verde'

    elif np.argmax(cor) ==2:
        color = 'Blue'

    #show the color on screem
    cv2.putText(frame, color, (10,50), 0, 1, (0,255,0),2)

    cv2.imshow("Eye of the robot", frame)

    print(color)


    
    

