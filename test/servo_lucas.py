from pyfirmata import Arduino, util
import time


porta_serial = 'COM1'

board = Arduino(porta_serial) #change Port

# Configuração dos pinos para os servos
# servo1 = board.get_pin('a:A1:s')  # Comprimento
# servo2 = board.get_pin('a:A5:s')  # Garra
# servo3 = board.get_pin('a:A3:s')  # Rotação
# servo4 = board.get_pin('a:A4:s')  # Altura

servo1 = board.digital[9] #change pin
servo2 = board.digital[10] #change pin
servo3 = board.digital[11] #change pin
servo4 = board.digital[12] #change pin

#servo1 = board.digital[9] #change pin
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

# Função para configurar a posição inicial
def pos_inicial():
    pino_servo4.write(pos_i4)
    pino_servo1.write(pos_i1)
    time.sleep(1.5)
    pino_servo2.write(pos_i2)
    time.sleep(1.5)
    pino_servo3.write(pos_i3)
    time.sleep(1.5)

# Função para pegar o objeto
def pegar_objeto():
    pos_negativa = 60
    for pos in range(60, pos_o4_1 + 1):
        if pos <= pos_o1_1:
            pino_servo1.write(pos)  # Esticar
        pino_servo4.write(pos)  # Altura
        time.sleep(0.015)
   
    time.sleep(1)
    pino_servo2.write(pos_o2)  
    time.sleep(1)
    pino_servo4.write(pos_o4_2)
    pino_servo1.write(pos_o1_2)

# Função para posicionar a caixa azul
def caixa_azul():
    pos_negativa = 60
    for pos in range(60, pos_caixa_azul3 + 1):
        if pos <= pos_caixa_azul1:
            pino_servo1.write(pos)
            pos_negativa -= 1
        if pos_negativa >= pos_caixa_azul4:
            pino_servo4.write(pos_negativa)
        pino_servo3.write(pos)
        time.sleep(0.015)

    time.sleep(0.5)
    pino_servo2.write(pos_caixa_azul2)
    time.sleep(0.5)
    pino_servo3.write(pos_i3)

# Função para posicionar a caixa vermelha
def caixa_vermelha():
    pos_positiva = 60
    for pos in range(60, pos_caixa_vermelha3 - 1, -1):
        if pos_positiva <= pos_caixa_vermelha1:
            pino_servo1.write(pos_positiva)
            pos_positiva += 10
        if pos >= pos_caixa_vermelha4:
            pino_servo4.write(pos)
        pino_servo3.write(pos)
        time.sleep(0.015)

    time.sleep(0.5)
    pino_servo2.write(pos_caixa_vermelha2)
    time.sleep(0.5)
    pino_servo3.write(pos_i3)

# Execução do código principal
if __name__ == "__main__":
    try:
        # Loop principal
        while True:
            pos_inicial()
            time.sleep(2)
            pegar_objeto()
            time.sleep(5)
            caixa_vermelha()
            time.sleep(5)

    except KeyboardInterrupt:
        #desligue os servos e feche a conexão com o Arduino.
        pino_servo1.write(pos_i1)
        pino_servo2.write(pos_i2)
        pino_servo3.write(pos_i3)
        pino_servo4.write(pos_i4)
