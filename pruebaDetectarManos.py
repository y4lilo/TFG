import cv2
import mediapipe as mp
import time

# Método para calcular la distancia euclidiana entre 2 puntos en la cámara
def distancia_euclidiana(p1, p2):
    d = ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) ** 0.5
    return d

# Explicación:
# - p1[0] y p1[1] representan las coordenadas x e y del primer punto. 
# - p2[0] y p2[1] representan las coordenadas x e y del segundo punto. 
# - (p1[0]-p2[0]): calcula la diferencia en la coordenada x.
# - (p1[1]-p2[1]): calcula la diferencia en la coordenada y. 
# - **2: calculan los cuadrados de estas diferencias. 
# - +: suma los cuadrados de las diferencias en x e y.
# - **0.5: es la raíz cuadrada, lo que devuelve la distancia entre los dos puntos. 



# Asociamos la cámara o dispositivo de captura a una variable
dispositivoCaptura = cv2.VideoCapture(0)

# Asignación para la detección de los puntos de la mano (visto en la imagen PuntosMano.png)
mpManos = mp.solutions.hands

# Creación de la instancia de detección de manos                     (0.1 la minima 1 la maxima)precisión
#                     Con esto indicamos que    | Con esto indicamos | Con esto indicamos cuanta      | Con esto hacemos el trackeo 
#                     va a ser una camara o un  | el número máximo   | certeza tiene que tener de     | de las manos
#                     video (no imagen sola)    | de manos           | que es una mano para mostrarlo |
manos = mpManos.Hands(static_image_mode = False, max_num_hands = 1,   min_detection_confidence = 0.9,   min_tracking_confidence = 0.9)

# Esto sirve para poder dibujar dentro de nuestro cuadro de cámara 
mpDibujo = mp.solutions.drawing_utils

# Esto sirve para darle estilo al dibujo
mpDrawingStyles = mp.solutions.drawing_styles

buffer_letras = ""
COOLDOWN = 2.0     # segundos mínimos entre detecciones
ultimo_detection_time = 0.0
ultimo_tiempo = time.time()

# Ahora un while true para poder capturar los frames de la cámara todo el rato
while True:
    succes, img = dispositivoCaptura.read()
    

    # 3) reseteo si no hay letras en 2 segundo
    if time.time() - ultimo_tiempo > 3.0:
        buffer_letras = ""

    
    img.flags.writeable = False
    # Pasamos la imagen capturada a rgb para que detecte bien las manos
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)# Convierte la imagen que detecta la cámara de BGR a RGB
    
    # Creamos una variable resultado que detecta si hay o si no hay manos
    resultado = manos.process(imgRGB)
    img.flags.writeable = True
    
    # Comprobamos si la mano detectada tiene varios landmarks (puntos de la mano de la imagen PuntosMano.png)
    if resultado.multi_hand_landmarks:
        # En caso de que si por cada landmark mostramos el punto
        for id, lm in enumerate(resultado.multi_hand_landmarks):
            mensaje_mostrar = ""
            mpDibujo.draw_landmarks(img, lm, mpManos.HAND_CONNECTIONS, mpDrawingStyles.get_default_hand_landmarks_style(), mpDrawingStyles.get_default_hand_connections_style()) # Captura la mano entera todo el rato
            # El id corresponde con los números de la imagen PuntosMano.png 
            # for id, lm in enumerate(handLms.landmark): # Captura cada dedo por separado
            
            alto, ancho, color = img.shape # Calculamos la posición en píxeles de la imagen
            # cx, cy = int(lm.x*ancho), int(lm.y*alto) # Calculamos donde debemos pintar el landmark (lm.x es la posición x de la detección de la imagen, y el lm.y la posicion y)
                
            index_finger_tip = (int(lm.landmark[8].x * ancho),
                                int(lm.landmark[8].y * alto))
            index_finger_pip = (int(lm.landmark[6].x * ancho),
                                int(lm.landmark[6].y * alto))
                
            thumb_tip = (int(lm.landmark[4].x * ancho),
                                int(lm.landmark[4].y * alto))
            thumb_pip = (int(lm.landmark[2].x * ancho),
                                int(lm.landmark[2].y * alto))
                
            middle_finger_tip = (int(lm.landmark[12].x * ancho),
                                int(lm.landmark[12].y * alto))
                
            middle_finger_pip = (int(lm.landmark[10].x * ancho),
                            int(lm.landmark[10].y * alto))
            
            ring_finger_tip = (int(lm.landmark[16].x * ancho),
                            int(lm.landmark[16].y * alto))
            ring_finger_pip = (int(lm.landmark[14].x * ancho),
                            int(lm.landmark[14].y * alto))
            
            pinky_tip = (int(lm.landmark[20].x * ancho),
                            int(lm.landmark[20].y * alto))
            pinky_pip = (int(lm.landmark[18].x * ancho),
                            int(lm.landmark[18].y * alto))
            
            wrist = (int(lm.landmark[0].x * ancho),
                            int(lm.landmark[0].y * alto))
            
            ring_finger_pip2 = (int(lm.landmark[5].x * ancho),
                            int(lm.landmark[5].y * alto))

            mensaje = ""
            
            if abs(thumb_tip[1] - index_finger_pip[1]) <45 \
                and abs(thumb_tip[1] - middle_finger_pip[1]) < 30 and abs(thumb_tip[1] - ring_finger_pip[1]) < 30\
                and abs(thumb_tip[1] - pinky_pip[1]) < 30:
                mensaje = "A"
                
                
            elif index_finger_pip[1] - index_finger_tip[1]>0 and pinky_pip[1] - pinky_tip[1] > 0 and \
                middle_finger_pip[1] - middle_finger_tip[1] >0 and ring_finger_pip[1] - ring_finger_tip[1] >0 and \
                    middle_finger_tip[1] - ring_finger_tip[1] <0 and abs(thumb_tip[1] - ring_finger_pip2[1])<40:
                mensaje = "B"
                
            elif abs(index_finger_tip[1] - thumb_tip[1]) < 360 and \
                index_finger_tip[1] - middle_finger_pip[1]<0 and index_finger_tip[1] - middle_finger_tip[1] < 0 and \
                    index_finger_tip[1] - index_finger_pip[1] > 0:
                mensaje = "C"
            
            elif distancia_euclidiana(thumb_tip, middle_finger_tip) < 65 \
                and distancia_euclidiana(thumb_tip, ring_finger_tip) < 65 \
                and  pinky_pip[1] - pinky_tip[1]<0\
                and index_finger_pip[1] - index_finger_tip[1]>0:
                mensaje = "D"
                
            elif index_finger_pip[1] - index_finger_tip[1] < 0 and pinky_pip[1] - pinky_tip[1] < 0 and \
                middle_finger_pip[1] - middle_finger_tip[1] < 0 and ring_finger_pip[1] - ring_finger_tip[1] < 0 \
                    and abs(index_finger_tip[1] - thumb_tip[1]) < 100 and \
                        thumb_tip[1] - index_finger_tip[1] > 0 \
                        and thumb_tip[1] - middle_finger_tip[1] > 0 \
                        and thumb_tip[1] - ring_finger_tip[1] > 0 \
                        and thumb_tip[1] - pinky_tip[1] > 0:

                mensaje = "E"
                
            elif  pinky_pip[1] - pinky_tip[1] > 0 and middle_finger_pip[1] - middle_finger_tip[1] > 0 and \
                ring_finger_pip[1] - ring_finger_tip[1] > 0 and index_finger_pip[1] - index_finger_tip[1] < 0 \
                    and abs(thumb_pip[1] - thumb_tip[1]) > 0 and distancia_euclidiana(index_finger_tip, thumb_tip) <65:
                mensaje = "F"

            now = time.time()
            if mensaje:
                if now - ultimo_detection_time >= COOLDOWN:
                    buffer_letras += mensaje
                    ultimo_detection_time = now
                    ultimo_tiempo = time.time()
                
            cv2.putText(img, buffer_letras, (0, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            3.0, (0, 0, 255), 6)

                
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

dispositivoCaptura.release()
cv2.destroyAllWindows()
    
                    # Ahora dependiendo de que dedo queramos mostrar pondremos un id u otro
                # if id == 4:
                #     cv2.circle(img, (cx,cy), 15, (225,0,225), cv2.FILLED)
                #     cv2.putText(img, "Pulgar", (20, alto - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            #     if id == 8:
            #         cv2.circle(img, (cx,cy), 15, (225,0,225), cv2.FILLED)
            #         cv2.putText(img, "Índice", (20, alto - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            #     if id == 12:
            #         cv2.circle(img, (cx,cy), 15, (225,0,225), cv2.FILLED)
            #         cv2.putText(img, "Medio", (20, alto - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            #     if id == 16:
            #         cv2.circle(img, (cx,cy), 15, (225,0,225), cv2.FILLED)
            #         cv2.putText(img, "Anular", (20, alto - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            #     if id == 20:
            #         cv2.circle(img, (cx,cy), 15, (225,0,225), cv2.FILLED)
            #         cv2.putText(img, "Meñique", (20, alto - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
