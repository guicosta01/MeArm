import cv2
import numpy as np



def detectar_formas(imagem):
    formato = ''
    # Converter a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplicar a detecção de bordas usando o algoritmo Canny
    bordas = cv2.Canny(imagem_cinza, 100, 200)

    # Encontrar contornos na imagem
    contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contorno in contornos:
        # Aproximar o contorno para uma forma com menos vértices
        epsilon = 0.04 * cv2.arcLength(contorno, True)
        forma_aproximada = cv2.approxPolyDP(contorno, epsilon, True)

        # Obter o número de vértices
        num_vertices = len(forma_aproximada)

        # Determinar a forma da figura com base no número de vértices
        if num_vertices == 4:
            # Se a figura tiver 4 vértices, ela é considerada um quadrado
            cv2.drawContours(imagem, [forma_aproximada], -1, (0, 255, 0), 2)
            formato = 'Quadrado'
        elif num_vertices > 4:
            # Se a figura tiver mais de 4 vértices, ela é considerada um círculo
            (x, y), raio = cv2.minEnclosingCircle(forma_aproximada)
            centro = (int(x), int(y))
            raio = int(raio)
            cv2.circle(imagem, centro, raio, (0, 0, 255), 2)
            formato = 'Circulo'

    return imagem,formato

# Inicializar a captura de vídeo (pode variar dependendo da sua câmera)
camera = cv2.VideoCapture(0)

while True:
    # Capturar o frame atual da câmera
    ret, frame = camera.read()

    # Verificar se o frame foi capturado corretamente
    if not ret:
        break

    # Redimensionar o frame para exibição
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

    # Detectar e desenhar formas na imagem
    imagem_com_formas,formato = detectar_formas(frame)

    # Exibir a imagem com as formas detectadas
    cv2.imshow('Detecção de Formas', imagem_com_formas)

    # Aguardar a tecla 'q' para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    print(formato)    
# Liberar a câmera e fechar todas as janelas abertas
camera.release()
cv2.destroyAllWindows()
