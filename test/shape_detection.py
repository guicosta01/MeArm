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

import cv2 

cap = cv2.VideoCapture(0)

format = ''

while True:
    
    ret, frame = cap.read()

    #(esc == 27) for quit
    key = cv2.waitKey(1)
    if key == 27:
        break


    #capturar cor apenas dentro de um retangulo     
    height,width,_ = frame.shape
    offset = 100
    campo = frame[offset:height-offset,offset:width-offset]
    #show rec 
    cv2.rectangle(frame,(offset,offset),(width-offset,height-offset),(255,0,0),3)

    gray_frame = cv2.cvtColor(campo, cv2.COLOR_BGR2GRAY) # Converting to gray frame

    # Setting threshold value to get new frame (In simpler terms: this function checks every pixel, and depending on how
    # dark the pixel is, the threshold value will convert the pixel to either black or white (0 or 1)).
    _, thresh_frame = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)

    # Retrieving outer-edge coordinates in the new threshold frame
    contours, hierarchy = cv2.findContours(thresh_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Iterating through each contour to retrieve coordinates of each shape
    for i, contour in enumerate(contours):
        if i == 0:
            continue

        # The 2 lines below this comment will approximate the shape we want. The reason being that in certain cases the
        # shape we want might have flaws or might be imperfect, and so, for example, if we have a rectangle with a
        # small piece missing, the program will still count it as a rectangle. The epsilon value will specify the
        # precision in which we approximate our shape.
        epsilon = 0.01*cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Drawing the outer-edges onto the frame
        cv2.drawContours(campo, contour, 0, (0, 0, 0), 4)

        # Retrieving coordinates of the contour so that we can put text over the shape.
        x, y, w, h= cv2.boundingRect(approx)
        x_mid = int(x + (w/3)) # This is an estimation of where the middle of the shape is in terms of the x-axis.
        y_mid = int(y + (h/1.5)) # This is an estimation of where the middle of the shape is in terms of the y-axis.

        # Setting some variables which will be used to display text on the final frame
        coords = (x_mid, y_mid)
        colour = (0, 0, 0)
        font = cv2.FONT_HERSHEY_DUPLEX

        # This is the part where we actually guess which shape we have detected. The program will look at the amount of edges
        # the contour/shape has, and then based on that result the program will guess the shape (for example, if it has 3 edges
        # then the chances that the shape is a triangle are very good.)
        #
        # You can add more shapes if you want by checking more lenghts, but for the simplicity of this tutorial program I
        # have decided to only detect 5 shapes.
        if len(approx) == 3:
            #cv2.putText(frame, "Triangle", coords, font, 1, colour, 1) # Text on the frame
            format = 'Triangle'
        elif len(approx) == 4:
            #cv2.putText(frame, "Quadrilateral", coords, font, 1, colour, 1)
            format = 'Quadrilateral'
        else:
            # If the length is not any of the above, we will guess the shape/contour to be a circle.
            #cv2.putText(frame, "Circle", coords, font, 1, colour, 1)
            format = 'Circle'
        
        # Displaying the frame with the detected shapes onto the screen
    cv2.putText(frame, format, (10,50), 0, 1, (0,255,0),2)    
    cv2.putText(frame, str(x_mid), (10,100), 0, 1, (0,0,255),2) 
    cv2.putText(frame, str(y_mid), (10,150), 0, 1, (255,0,0),2) 
    cv2.imshow("shapes_detected", frame)
    
    
        