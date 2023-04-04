import os
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import pyttsx3

cap = cv2.VideoCapture(1)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
labels = ["A", "B", "C", "D", "E", "_", "F", "G", "H",
          "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
          "S", "T", "U", "V", "W", "X", "Y", "Z"]
offset = 10
imgSize = 300
def Hablar(Texto):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    # Establecer la voz en español "Sabina"
    engine.setProperty("voice", voices[3].id)
    engine.setProperty('rate', 200)
    engine.say(Texto)
    engine.runAndWait()
def letras_abecedario(n):
    oracion = ""
    if n == 1:
        oracion = 'UPDS '
    elif n == 2:
        oracion = 'GRUPO '
    elif n == 3:
        oracion = 'APRENDER '
    elif n == 4:
        oracion = 'CELULAR '
    return oracion

#funciones
def tiempoReiniciar(timer1, imgOutput1, img1):
    # calcular el tiempo restante en segundos
    timer_text = "Tiempo: " + str(int(timer1)) + "s"
    cv2.putText(imgOutput1, timer_text,
                (img1.shape[1] - 200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
def tiempoInsertar(timer2, imgOutput2, img2):
    # calcular el tiempo restante en segundos
    timer_text = "Insertar en:" + str(int(timer2)) + "s"
    cv2.putText(imgOutput2, timer_text,
                (img2.shape[1] -630, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
n = 1
#letra = letras_abecedario(1)


def letraInsertar(imgOutput, position1, letra1):
    # Obtener la letra correspondiente
    TextoPantalla = letra1[position1]

    # Definir las coordenadas del rectángulo
    x, y = -1, 359
    w, h = cv2.getTextSize(TextoPantalla, cv2.FONT_HERSHEY_SIMPLEX, 5, 5)[0]

    # Dibujar el rectángulo en la imagen
    cv2.rectangle(imgOutput, (x, y), (x+w+10, y+h+10), (255, 255, 255), -1)

    # Dibujar el texto dentro del rectángulo
    cv2.putText(imgOutput, TextoPantalla, (x+5, y+h+5),
                cv2.FONT_HERSHEY_SIMPLEX, 5, (185, 70, 45), 5)




def ImagenInsertar(nombre_imagen):
    # Concatenar la extensión ".jpg" al nombre de la imagen
    nombre_imagen += ".jpeg"

    # Cargar la imagen desde la carpeta "Img"
    ruta_imagen = os.path.join("Img", nombre_imagen)
    imagen = cv2.imread(ruta_imagen)

    # Mostrar la imagen en una nueva ventana y redimensionarla
    cv2.namedWindow("Pantalla mano", cv2.WINDOW_NORMAL)
    cv2.imshow("Pantalla mano", imagen)
    cv2.resizeWindow("Pantalla mano", 400, 500)

timer = 200
TimepoEspera = 10
word = ""
position = 0


def Bucle(classifier2, labels2, timer2, word2, TimepoEspera2, position2):
    n1 = 1
    letra = letras_abecedario(1)
    activarImage = True
    while True:
        success, img = cap.read()
        imgOutput = img.copy()
        hands, img = detector.findHands(img)
        try:
            if activarImage:
                print(letra[position2])
                ImagenInsertar(letra[position2])
                activarImage = False
        except Exception as e:
            print("Error al insertar imagen:", e)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
            # Obtener la forma del recorte
            aspectRatio = h / w
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
                prediction, index = classifier2.getPrediction(
                    imgWhite, draw=False)
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier2.getPrediction(
                    imgWhite, draw=False)
            #Cromometro
            print(index)
            if timer2 == 0:
                #print("Perdiste")
                Hablar("Perdiste")
                timer2 = timer
                cv2.destroyAllWindows()
                cap.release()
                import Inicio     
                break       
            else:
                timer2 -= 1
            #print(timer2)
            if position2 < len(letra) - 1:
                if labels2[index] == letra[position2]:
                    if TimepoEspera2 == 0:
                            position2 += 1
                            word2 += labels2[index]
                            TimepoEspera2 = TimepoEspera
                            timer2 = timer  
                            activarImage = True
                            Hablar("Letra escrita")
                    else:
                        TimepoEspera2 -= 1
                        #print(TimepoEspera2)
                else:
                    TimepoEspera2 = TimepoEspera
            else:
                Hablar("Excelente, siguiente palabra")
                n1 += 1
                activarImage = True
                position2 = 0
                word2 = " "
                letra = letras_abecedario(n1)           
            cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                          (x - offset+90, y - offset-50+50), (185, 70, 45), cv2.FILLED)
            cv2.putText(imgOutput, labels2[index], (x, y - 26),
                        cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x-offset, y-offset),
                          (x + w+offset, y + h+offset), (185, 70, 45), 4)
            cv2.rectangle(imgOutput, (x-offset, y-offset),
                          (x + w+offset, y + h+offset), (185, 70, 45), 4)
        # Mostrar la palabra formada
        cv2.rectangle(imgOutput, (0, 0),
                      (img.shape[1], 50), (185, 70, 45), cv2.FILLED)
        cv2.putText(imgOutput, word2, (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        tiempoReiniciar(timer2, imgOutput, img)
        tiempoInsertar(TimepoEspera2, imgOutput, img)
        letraInsertar(imgOutput, position2, letra)
        cv2.imshow("Pantalla", imgOutput)
        # Salir del bucle al presionar
        if cv2.waitKey(1) == ord('q'):
            break
        elif cv2.waitKey(1) == ord('e'):
            Hablar(word2)
        elif cv2.waitKey(1) == ord('b'):
            word2 = word2[:-1]
        elif cv2.waitKey(1) == ord('t'):
            word2 = ""

Bucle(classifier, labels, timer, word, TimepoEspera,position)
cv2.destroyAllWindows()
cap.release()
