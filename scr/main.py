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

from pyfirmata import Arduino, util, SERVO
import time
import numpy as np
import cv2

#DEFINES / CONST
porta_serial = 'COM5'

board = Arduino(porta_serial) #change Port

#Configuração dos pinos para os servos
servo1 = board.get_pin('d:10:o') # Comprimento
servo2 = board.get_pin('d:4:o')  # Garra
servo3 = board.get_pin('d:9:o')  # Rotação
servo4 = board.get_pin('d:7:o')  # Altura

servo1.mode = SERVO
servo2.mode = SERVO
servo3.mode = SERVO
servo4.mode = SERVO

# Posições iniciais
pos_i1 = 30
pos_i2 = 5
pos_i3 = 95
pos_i4 = 80

# Posições do objeto
pos_o1_1 = 75  # Esticar
pos_o1_2 = 40  # Volta
pos_o2 = 85  # Fechar garra
pos_o4_1 = 120  # Esticar
pos_o4_2 = 90  # Volta

# Posições caixa azul
pos_caixa_azul1 = 230
pos_caixa_azul2 = 5
pos_caixa_azul3 = 230
pos_caixa_azul4 = 60

# Posições caixa vermelha
pos_caixa_vermelha1 = 200
pos_caixa_vermelha2 = 5
pos_caixa_vermelha3 = 5
pos_caixa_vermelha4 = 60

cap = cv2.VideoCapture(1)
color = ''
shape = ''
dist = lambda x1,y1,x2,y2: (x1-x2)**2 + (y1-y2)**2
prevcircle = None

# Função para configurar a posição inicial
def pos_inicial():
    servo4.write(pos_i4)
    servo1.write(pos_i1)
    time.sleep(1.5)
    servo2.write(pos_i2)
    time.sleep(1.5)
    servo3.write(pos_i3)
    time.sleep(1.5)

# Função para pegar o objeto
def pegar_objeto():
    pos_negativa = 60
    for pos in range(60, pos_o4_1 + 1):
        if pos <= pos_o1_1:
            servo1.write(pos)  # Esticar
        servo4.write(pos)  # Altura
        time.sleep(0.015)
   
    time.sleep(1)
    servo2.write(pos_o2)  
    time.sleep(1)
    servo4.write(pos_o4_2)
    servo1.write(pos_o1_2)

# Função para posicionar a caixa azul
def caixa_azul():
    pos_negativa = 60
    for pos in range(60, pos_caixa_azul3 + 1):
        if pos <= pos_caixa_azul1:
            servo1.write(pos)

        if pos_negativa >= pos_caixa_azul4:
            servo4.write(pos_negativa)
            pos_negativa -= 1
        servo3.write(pos)
        time.sleep(0.015)

    time.sleep(0.5)
    servo2.write(pos_caixa_azul2)
    time.sleep(0.5)
    servo3.write(pos_i3)

# Função para posicionar a caixa vermelha
def caixa_vermelha():
    pos_positiva = 60
    for pos in range(60, pos_caixa_vermelha3 - 1, -1):
        if pos_positiva <= pos_caixa_vermelha1:
            servo1.write(pos_positiva)
            pos_positiva += 10
        if pos >= pos_caixa_vermelha4:
            servo4.write(pos)
        servo3.write(pos)
        time.sleep(0.015)

    time.sleep(0.5)
    servo2.write(pos_caixa_vermelha2)
    time.sleep(0.5)
    servo3.write(pos_i3)

def get_color():
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
        
        # if r >=140 and g>=140 and b <=60:
        #     color = 'Amarelo'
            
        if np.argmax(cor) ==0:
            color = 'Vermelho'

        elif np.argmax(cor) ==1:
            color = 'Verde'

        elif np.argmax(cor) ==2:
            color = 'Azul'

        #show the color on screem
        cv2.putText(frame, color, (10,50), 0, 1, (0,255,0),2)

        cv2.imshow("Eye of the robot", frame)

    return color

def get_shape():
    while True:
        ret, frame = cap.read()

        prevcircle = None
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

            #cv2.putText(frame, str(dist), (10,50), 0, 1, (0,255,0),2)


        if circles is None:
            cv2.putText(frame, 'Square', (10,50), 0, 1, (0,255,0),2)
            shape = 'Cubo'
        else:
            shape = 'Esfera'    


        #param1 - baixo acha mt circulo
        cv2.imshow("Eye of the robot", frame)
    return shape

def main():
    var = True
    while var:
        print("\n-----------------------------------------")
        print("MeArm")
        print("-----------------------------------------")
        try:
            print('1 -> cor/shape')
            print('2 -> pega obj')
            print('3 -> guarda obj')
            print("-----------------------------------------")

            aux = int(input('Digite um número: '))

            if (aux == 1):
                print("Detectando cor...")

                aux_color = get_color()
                print(aux_color)
                print("\n-----------------------------------------")
                print("Detectando forma...\n")
                aux_shape = get_shape()
                print(aux_shape)

            elif(aux ==2):
                print('Pega obj\n')
                pos_inicial()
                pegar_objeto()
            elif(aux ==3):
                if(aux_color == 'Azul'):
                    caixa_azul()
                if(aux_color == 'Vermelho'):
                    caixa_vermelha()
            else: 
                print('sair\n')
                var = False    
                

        except KeyboardInterrupt:
            #volta pos inicial 
            servo1.write(pos_i1)
            servo2.write(pos_i2)
            servo3.write(pos_i3)
            servo4.write(pos_i4)


if __name__ == '__main__':
    main()
    