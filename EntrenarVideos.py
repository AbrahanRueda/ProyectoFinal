import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

# Tamaño del cuadro blanco
imgSize = 300

# Desplazamiento para recortar la mano
offset = 20

folder = "Letras/Z"
counter = 0

is_recording = False
out = None

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        # Obtener la posición de la mano
        hand = hands[0]
        x, y, w, h = hand['bbox']

        # Crear un cuadro blanco
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

        # Recortar la mano
        imgCrop = img[max(0, y - offset):min(y + h + offset, img.shape[0]),
                      max(0, x - offset):min(x + w + offset, img.shape[1])]

        # Obtener la forma del recorte
        imgCropShape = imgCrop.shape

        # Verificar que el recorte no sea más grande que el cuadro blanco
        if imgCropShape[0] > imgSize or imgCropShape[1] > imgSize:
            continue
        aspectRatio = h / w
        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgCrop.shape
            wGap = math.ceil((imgSize-wCal)/2)
            imgWhite[0:imgSize, wGap:wCal + wGap] = imgResize
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize-hCal)/2)
            imgWhite[hGap:hCal + hGap, 0:imgSize] = imgResize

        cv2.imshow("Crop", imgCrop)
        cv2.imshow("White", imgWhite)

        # Empezar a grabar al presionar la tecla "r"
        if cv2.waitKey(1) == ord('r'):
            if not is_recording:
                is_recording = True
                counter += 1
                out = cv2.VideoWriter(f"{folder}/Video_{time.time()}.avi",
                                      cv2.VideoWriter_fourcc(*'XVID'), 30.0, (imgSize, imgSize))
                print("Empezando a grabar...")

        # Detener la grabación al presionar la tecla "s"
        if cv2.waitKey(1) == ord('s'):
            if is_recording:
                is_recording = False
                out.release()
                print(f"Video guardado: {counter}")

        # Guardar el frame actual en el video si se está grabando
        if is_recording:
            out.write(imgWhite)

    cv2.imshow("Image", img)


    # Salir del bucle al presionar la tecla "q"
    if cv2.waitKey(1) == ord('q'):
        break

# Liberar todo cuando se acabe
cap.release()
cv2.destroyAllWindows()
