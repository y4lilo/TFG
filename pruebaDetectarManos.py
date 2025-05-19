import cv2
import mediapipe as mp
import time
import math 
    
# -----------------------------------------------------------------------------
# MÉTODO PARA CALCULAR LA DISTANCIA ENTRE 2 PUNTOS (sin cambios)
# -----------------------------------------------------------------------------
def calcular_distancia(p1, p2):
    """
    Calcula la distancia euclidiana entre dos puntos en un espacio 2D.
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Explicación:
# - p1[0] y p1[1] representan las coordenadas x e y del primer punto. 
# - p2[0] y p2[1] representan las coordenadas x e y del segundo punto. 
# - (p1[0]-p2[0]): calcula la diferencia en la coordenada x.
# - (p1[1]-p2[1]): calcula la diferencia en la coordenada y. 
# - **2: calculan los cuadrados de estas diferencias. 
# - +: suma los cuadrados de las diferencias en x e y.
# - **0.5: es la raíz cuadrada, lo que devuelve la distancia entre los dos puntos. 

# -----------------------------------------------------------------------------
# MÉTODOS PARA SABER SI UN DEDO ESTÁ LEVANTADO (MANO VERTICAL) (sin cambios)
# -----------------------------------------------------------------------------
def pulgar_levantado_vertical(thumb_tip, thumb_ip, thumb_mcp, umbral_relativo_mcp=15, umbral_relativo_ip=5):
    if thumb_tip[1] < thumb_mcp[1] - umbral_relativo_mcp and \
       thumb_tip[1] < thumb_ip[1] - umbral_relativo_ip:
        return True
    return False

def indice_levantado_vertical(index_tip, index_pip, index_mcp, umbral_relativo_mcp=20, umbral_relativo_pip=10):
    return index_tip[1] < index_mcp[1] - umbral_relativo_mcp and \
           index_tip[1] < index_pip[1] - umbral_relativo_pip

def medio_levantado_vertical(middle_tip, middle_pip, middle_mcp, umbral_relativo_mcp=20, umbral_relativo_pip=10):
    return middle_tip[1] < middle_mcp[1] - umbral_relativo_mcp and \
           middle_tip[1] < middle_pip[1] - umbral_relativo_pip

def anular_levantado_vertical(ring_tip, ring_pip, ring_mcp, umbral_relativo_mcp=20, umbral_relativo_pip=10):
    return ring_tip[1] < ring_mcp[1] - umbral_relativo_mcp and \
           ring_tip[1] < ring_pip[1] - umbral_relativo_pip

def menique_levantado_vertical(pinky_tip, pinky_pip, pinky_mcp, umbral_relativo_mcp=15, umbral_relativo_pip=8):
    return pinky_tip[1] < pinky_mcp[1] - umbral_relativo_mcp and \
           pinky_tip[1] < pinky_pip[1] - umbral_relativo_pip

# -----------------------------------------------------------------------------
# MÉTODOS PARA SABER SI UN DEDO ESTÁ EXTENDIDO (MANO HORIZONTAL)
# -----------------------------------------------------------------------------
# Asumimos:
# - Mano orientada horizontalmente.
# - "Extendido horizontalmente" significa que la punta del dedo está significativamente
#   más a la izquierda/derecha que su articulación base (MCP).
# - Adicionalmente, la diferencia en Y entre tip, pip y mcp debe ser pequeña (dedo recto horizontalmente).
# - Los umbrales (ej. `umbral_y_alineado`) son para asegurar que el dedo no esté muy curvado verticalmente.

# --- HACIA LA IZQUIERDA (Dedos apuntan a la izquierda del marco) ---

def pulgar_extendido_horizontal_izquierda(thumb_tip, thumb_ip, thumb_mcp, umbral_extension_x=15, umbral_y_alineado=20):
    """
    Verifica si el pulgar está extendido horizontalmente hacia la izquierda.
    La coordenada Y del pulgar tip debe estar relativamente alineada con su MCP.
    """
    y_alineado_pulgar = abs(thumb_tip[1] - thumb_mcp[1]) < umbral_y_alineado
    # El pulgar extendido hacia la izquierda suele estar por encima (menor Y) de los otros dedos o alineado.
    # Aquí nos centramos en la extensión X y la alineación Y general del pulgar en sí.
    return thumb_tip[0] < thumb_mcp[0] - umbral_extension_x and \
           thumb_tip[0] < thumb_ip[0] - (umbral_extension_x * 0.5) and \
           y_alineado_pulgar

def indice_extendido_horizontal_izquierda(index_tip, index_pip, index_mcp, umbral_extension_x=20, umbral_y_alineado=15):
    """
    Verifica si el dedo índice está extendido horizontalmente hacia la izquierda.
    """
    y_alineado = abs(index_tip[1] - index_pip[1]) < umbral_y_alineado and \
                 abs(index_pip[1] - index_mcp[1]) < umbral_y_alineado
    return index_tip[0] < index_mcp[0] - umbral_extension_x and \
           index_tip[0] < index_pip[0] - (umbral_extension_x * 0.5) and \
           y_alineado

def medio_extendido_horizontal_izquierda(middle_tip, middle_pip, middle_mcp, umbral_extension_x=20, umbral_y_alineado=15):
    """
    Verifica si el dedo medio está extendido horizontalmente hacia la izquierda.
    """
    y_alineado = abs(middle_tip[1] - middle_pip[1]) < umbral_y_alineado and \
                 abs(middle_pip[1] - middle_mcp[1]) < umbral_y_alineado
    return middle_tip[0] < middle_mcp[0] - umbral_extension_x and \
           middle_tip[0] < middle_pip[0] - (umbral_extension_x * 0.5) and \
           y_alineado

def anular_extendido_horizontal_izquierda(ring_tip, ring_pip, ring_mcp, umbral_extension_x=20, umbral_y_alineado=15):
    """
    Verifica si el dedo anular está extendido horizontalmente hacia la izquierda.
    """
    y_alineado = abs(ring_tip[1] - ring_pip[1]) < umbral_y_alineado and \
                 abs(ring_pip[1] - ring_mcp[1]) < umbral_y_alineado
    return ring_tip[0] < ring_mcp[0] - umbral_extension_x and \
           ring_tip[0] < ring_pip[0] - (umbral_extension_x * 0.5) and \
           y_alineado

def menique_extendido_horizontal_izquierda(pinky_tip, pinky_pip, pinky_mcp, umbral_extension_x=15, umbral_y_alineado=12):
    """
    Verifica si el dedo meñique está extendido horizontalmente hacia la izquierda.
    """
    y_alineado = abs(pinky_tip[1] - pinky_pip[1]) < umbral_y_alineado and \
                 abs(pinky_pip[1] - pinky_mcp[1]) < umbral_y_alineado
    return pinky_tip[0] < pinky_mcp[0] - umbral_extension_x and \
           pinky_tip[0] < pinky_pip[0] - (umbral_extension_x * 0.5) and \
           y_alineado

# --- HACIA LA DERECHA (Dedos apuntan a la derecha del marco) ---

def pulgar_extendido_horizontal_derecha(thumb_tip, thumb_ip, thumb_mcp, umbral_extension_x=15, umbral_y_alineado=20):
    """
    Verifica si el pulgar está extendido horizontalmente hacia la derecha.
    """
    y_alineado_pulgar = abs(thumb_tip[1] - thumb_mcp[1]) < umbral_y_alineado
    return thumb_tip[0] > thumb_mcp[0] + umbral_extension_x and \
           thumb_tip[0] > thumb_ip[0] + (umbral_extension_x * 0.5) and \
           y_alineado_pulgar

def indice_extendido_horizontal_derecha(index_tip, index_pip, index_mcp, umbral_extension_x=20, umbral_y_alineado=15):
    """
    Verifica si el dedo índice está extendido horizontalmente hacia la derecha.
    """
    y_alineado = abs(index_tip[1] - index_pip[1]) < umbral_y_alineado and \
                 abs(index_pip[1] - index_mcp[1]) < umbral_y_alineado
    return index_tip[0] > index_mcp[0] + umbral_extension_x and \
           index_tip[0] > index_pip[0] + (umbral_extension_x * 0.5) and \
           y_alineado

def medio_extendido_horizontal_derecha(middle_tip, middle_pip, middle_mcp, umbral_extension_x=20, umbral_y_alineado=15):
    """
    Verifica si el dedo medio está extendido horizontalmente hacia la derecha.
    """
    y_alineado = abs(middle_tip[1] - middle_pip[1]) < umbral_y_alineado and \
                 abs(middle_pip[1] - middle_mcp[1]) < umbral_y_alineado
    return middle_tip[0] > middle_mcp[0] + umbral_extension_x and \
           middle_tip[0] > middle_pip[0] + (umbral_extension_x * 0.5) and \
           y_alineado

def anular_extendido_horizontal_derecha(ring_tip, ring_pip, ring_mcp, umbral_extension_x=20, umbral_y_alineado=15):
    """
    Verifica si el dedo anular está extendido horizontalmente hacia la derecha.
    """
    y_alineado = abs(ring_tip[1] - ring_pip[1]) < umbral_y_alineado and \
                 abs(ring_pip[1] - ring_mcp[1]) < umbral_y_alineado
    return ring_tip[0] > ring_mcp[0] + umbral_extension_x and \
           ring_tip[0] > ring_pip[0] + (umbral_extension_x * 0.5) and \
           y_alineado

def menique_extendido_horizontal_derecha(pinky_tip, pinky_pip, pinky_mcp, umbral_extension_x=15, umbral_y_alineado=12):
    """
    Verifica si el dedo meñique está extendido horizontalmente hacia la derecha.
    """
    y_alineado = abs(pinky_tip[1] - pinky_pip[1]) < umbral_y_alineado and \
                 abs(pinky_pip[1] - pinky_mcp[1]) < umbral_y_alineado
    return pinky_tip[0] > pinky_mcp[0] + umbral_extension_x and \
           pinky_tip[0] > pinky_pip[0] + (umbral_extension_x * 0.5) and \
           y_alineado


def obtener_orientacion_mano(wrist_coords, middle_finger_mcp_coords, ratio_threshold=1.5):
    """
    Determina la orientación predominante de la mano (vertical u horizontal).

    Args:
        wrist_coords: Tupla (x, y) de las coordenadas de la muñeca (landmark 0).
        middle_finger_mcp_coords: Tupla (x, y) de las coordenadas del nudillo MCP
                                   del dedo medio (landmark 9).
        ratio_threshold: Umbral para decidir si una orientación es dominante.
                         Un valor > 1. Si abs(delta_y)/abs(delta_x) > ratio_threshold,
                         se considera vertical. Si abs(delta_x)/abs(delta_y) > ratio_threshold,
                         se considera horizontal. Un valor de 1.5 a 2.0 suele funcionar bien.

    Returns:
        Un string indicando la orientación:
        - "VERTICAL"
        - "HORIZONTAL_IZQUIERDA" (dedos apuntan predominantemente a la izquierda)
        - "HORIZONTAL_DERECHA" (dedos apuntan predominantemente a la derecha)
        - "DIAGONAL_INDETERMINADA" (si no es claramente vertical ni horizontal)
        - "INDETERMINADA_ESTATICA" (si los puntos son casi idénticos)
    """
    delta_x = middle_finger_mcp_coords[0] - wrist_coords[0]
    # En la mayoría de las configuraciones de imagen, Y disminuye hacia arriba.
    # Por lo tanto, si mcp_middle está "encima" de wrist, delta_y será negativo.
    delta_y = middle_finger_mcp_coords[1] - wrist_coords[1]

    abs_delta_x = abs(delta_x)
    abs_delta_y = abs(delta_y)

    # Evitar división por cero o valores muy pequeños si los puntos están muy juntos
    epsilon = 1e-6 # Un valor muy pequeño

    if abs_delta_x < epsilon and abs_delta_y < epsilon:
        return "INDETERMINADA_ESTATICA" # Puntos casi idénticos

    # Caso predominantemente VERTICAL
    # (abs_delta_y es significativamente mayor que abs_delta_x)
    if abs_delta_x < epsilon: # Prácticamente vertical puro
        return "VERTICAL"
    if abs_delta_y / abs_delta_x > ratio_threshold:
        return "VERTICAL"

    # Caso predominantemente HORIZONTAL
    # (abs_delta_x es significativamente mayor que abs_delta_y)
    if abs_delta_y < epsilon: # Prácticamente horizontal puro
        if delta_x > 0: # MCP del medio a la derecha de la muñeca -> dedos a la derecha
            return "HORIZONTAL_DERECHA"
        else: # MCP del medio a la izquierda de la muñeca -> dedos a la izquierda
            return "HORIZONTAL_IZQUIERDA"

    if abs_delta_x / abs_delta_y > ratio_threshold:
        if delta_x > 0: # MCP del medio a la derecha de la muñeca
            return "HORIZONTAL_DERECHA"
        else: # MCP del medio a la izquierda de la muñeca
            return "HORIZONTAL_IZQUIERDA"

    # Si no es claramente vertical ni horizontal según el umbral
    return "DIAGONAL_INDETERMINADA"





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

# --- (Al inicio de tu script, antes del bucle while True) ---
previous_pinky_tip_j = None
previous_index_tip_z = None
MOTION_THRESHOLD_J = 10 # Ajustar
MOTION_THRESHOLD_Z = 15 # Ajustar

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
                
            # Tips (Puntas de los dedos)
            thumb_tip = (int(lm.landmark[4].x * ancho), int(lm.landmark[4].y * alto))
            index_tip = (int(lm.landmark[8].x * ancho), int(lm.landmark[8].y * alto))
            middle_tip = (int(lm.landmark[12].x * ancho), int(lm.landmark[12].y * alto))
            ring_tip = (int(lm.landmark[16].x * ancho), int(lm.landmark[16].y * alto))
            pinky_tip = (int(lm.landmark[20].x * ancho), int(lm.landmark[20].y * alto))

            # PIP (Articulación interfalángica proximal - la del medio de los dedos largos)
            thumb_ip = (int(lm.landmark[3].x * ancho), int(lm.landmark[3].y * alto)) # Para el pulgar, es la IP
            index_pip = (int(lm.landmark[6].x * ancho), int(lm.landmark[6].y * alto))
            middle_pip = (int(lm.landmark[10].x * ancho), int(lm.landmark[10].y * alto))
            ring_pip = (int(lm.landmark[14].x * ancho), int(lm.landmark[14].y * alto))
            pinky_pip = (int(lm.landmark[18].x * ancho), int(lm.landmark[18].y * alto))

            # DIP (Articulación interfalángica distal - la más cercana a la punta)
            index_dip = (int(lm.landmark[7].x * ancho), int(lm.landmark[7].y * alto))
            middle_dip = (int(lm.landmark[11].x * ancho), int(lm.landmark[11].y * alto))
            ring_dip = (int(lm.landmark[13].x * ancho), int(lm.landmark[13].y * alto))
            pinky_dip = (int(lm.landmark[19].x * ancho), int(lm.landmark[19].y * alto))

            # MCP (Articulación metacarpofalángica - los nudillos)
            thumb_mcp = (int(lm.landmark[2].x * ancho), int(lm.landmark[2].y * alto)) 
            index_mcp = (int(lm.landmark[5].x * ancho), int(lm.landmark[5].y * alto))
            middle_mcp = (int(lm.landmark[9].x * ancho), int(lm.landmark[9].y * alto))
            ring_mcp = (int(lm.landmark[13].x * ancho), int(lm.landmark[13].y * alto))
            pinky_mcp = (int(lm.landmark[17].x * ancho), int(lm.landmark[17].y * alto))

            wrist = (int(lm.landmark[0].x * ancho), int(lm.landmark[0].y * alto))
            
            # Índice
            indice_extendidoHD = indice_extendido_horizontal_derecha(index_tip, index_pip, index_mcp)
            indice_extendidoHI = indice_extendido_horizontal_izquierda(index_tip, index_pip, index_mcp)
            indice_extendidoV = indice_levantado_vertical(index_tip, index_pip, index_mcp)
            # Medio
            corazon_extendidoHD = medio_extendido_horizontal_derecha(middle_tip, middle_pip, middle_mcp)
            corazon_extendidoHI = medio_extendido_horizontal_izquierda(middle_tip, middle_pip, middle_mcp)
            corazon_extendidoV = medio_levantado_vertical(middle_tip, middle_pip, middle_mcp)
            # Anular
            anular_extendidoHD = anular_extendido_horizontal_derecha(ring_tip, ring_pip, ring_mcp)
            anular_extendidoHI = anular_extendido_horizontal_izquierda(ring_tip, ring_pip, ring_mcp)
            anular_extendidoV = anular_levantado_vertical(ring_tip, ring_pip, ring_mcp)
            # Meñique
            meñique_extendidoHD = menique_extendido_horizontal_derecha(pinky_tip, pinky_pip, pinky_mcp)
            meñique_extendidoHI = menique_extendido_horizontal_izquierda(pinky_tip, pinky_pip, pinky_mcp)
            meñique_extendidoV = menique_levantado_vertical(pinky_tip, pinky_pip, pinky_mcp)
            # Pulgar
            pulgar_extendidoHD = pulgar_extendido_horizontal_derecha(thumb_tip, thumb_ip, thumb_mcp)
            pulgar_extendidoHI = pulgar_extendido_horizontal_izquierda(thumb_tip, thumb_ip, thumb_mcp)
            pulgar_extendidoV = pulgar_levantado_vertical(thumb_tip, thumb_ip, thumb_mcp)
           
            mensaje = ""
            
            if obtener_orientacion_mano(wrist, middle_mcp)=="VERTICAL":
                if not indice_extendidoV and not corazon_extendidoV and not anular_extendidoV and not meñique_extendidoV and not pulgar_extendidoV  and not pulgar_extendidoHD and not pulgar_extendidoHI:
                    mensaje="A"
                # elif abs(index_tip[1] - thumb_tip[1]) < 360 and index_tip[1] - middle_pip[1]<0 and index_tip[1] - middle_tip[1] < 0 and index_tip[1] - index_pip[1] > 0:
                #     mensaje = "C"
                elif abs(middle_tip[1] - thumb_tip[1]) < 10 and abs(ring_tip[1] - thumb_tip[1]) < 10 and (meñique_extendidoHI or meñique_extendidoHD) and indice_extendidoV: 
                    mensaje = "D"
                elif not indice_extendidoV and not corazon_extendidoV and not anular_extendidoV and not meñique_extendidoV and \
                    thumb_tip[1] > index_dip[1] and thumb_tip[1] > middle_dip[1] and thumb_tip[1] > ring_dip[1] and thumb_tip[1] > pinky_dip[1]: # Si todos están hacia abajo y la punta del pulgar está más alto que todos es la E
                    mensaje = "E"
           
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
            
            
            
            #   if abs(thumb_tip[1] - index_finger_pip[1]) <45 \
            #     and abs(thumb_tip[1] - middle_finger_pip[1]) < 30 and abs(thumb_tip[1] - ring_finger_pip[1]) < 30\
            #     and abs(thumb_tip[1] - pinky_pip[1]) < 30:
            #     mensaje = "A"
                
                
            # elif index_finger_pip[1] - index_finger_tip[1]>0 and pinky_pip[1] - pinky_tip[1] > 0 and \
            #     middle_finger_pip[1] - middle_finger_tip[1] >0 and ring_finger_pip[1] - ring_finger_tip[1] >0 and \
            #         middle_finger_tip[1] - ring_finger_tip[1] <0 and abs(thumb_tip[1] - ring_finger_pip2[1])<40:
            #     mensaje = "B"
                
            # elif abs(index_finger_tip[1] - thumb_tip[1]) < 360 and \
            #     index_finger_tip[1] - middle_finger_pip[1]<0 and index_finger_tip[1] - middle_finger_tip[1] < 0 and \
            #         index_finger_tip[1] - index_finger_pip[1] > 0:
            #     mensaje = "C"
            
            # elif distancia_euclidiana(thumb_tip, middle_finger_tip) < 65 \
            #     and distancia_euclidiana(thumb_tip, ring_finger_tip) < 65 \
            #     and  pinky_pip[1] - pinky_tip[1]<0\
            #     and index_finger_pip[1] - index_finger_tip[1]>0:
            #     mensaje = "D"
                
            # elif index_finger_pip[1] - index_finger_tip[1] < 0 and pinky_pip[1] - pinky_tip[1] < 0 and \
            #     middle_finger_pip[1] - middle_finger_tip[1] < 0 and ring_finger_pip[1] - ring_finger_tip[1] < 0 \
            #         and abs(index_finger_tip[1] - thumb_tip[1]) < 100 and \
            #             thumb_tip[1] - index_finger_tip[1] > 0 \
            #             and thumb_tip[1] - middle_finger_tip[1] > 0 \
            #             and thumb_tip[1] - ring_finger_tip[1] > 0 \
            #             and thumb_tip[1] - pinky_tip[1] > 0:

            #     mensaje = "E"
                
            # elif  pinky_pip[1] - pinky_tip[1] > 0 and middle_finger_pip[1] - middle_finger_tip[1] > 0 and \
            #     ring_finger_pip[1] - ring_finger_tip[1] > 0 and index_finger_pip[1] - index_finger_tip[1] < 0 \
            #         and abs(thumb_pip[1] - thumb_tip[1]) > 0 and distancia_euclidiana(index_finger_tip, thumb_tip) <65:
            #     mensaje = "F"






# --- LÓGICA DE DETECCIÓN ---
            # # Priorizar señas más distintivas o con movimiento primero
            
            # # --- A ---
            # # Puño, pulgar al lado del índice, tocando o casi. Todos los dedos flexionados.
            # # Yemas de los dedos (index, middle, ring, pinky) deben estar más bajas que sus PIPs
            # # Pulgar NO debe formar parte de un círculo con el índice (diferencia de O)
            # # Pulgar tip[1] similar a index_finger_pip[1]
            # if not mensaje: # Solo si no se detectó nada con movimiento
            #     if index_flexed and middle_flexed and ring_flexed and pinky_flexed and \
            #        abs(thumb_tip[1] - index_finger_pip[1]) < 30 and \
            #        thumb_tip[0] < index_finger_pip[0] and \
            #        distancia_euclidiana(thumb_tip, index_finger_pip) < 50 and \
            #        distancia_euclidiana(thumb_tip, index_finger_tip) > 40: # Evitar O
            #         mensaje = "A"
            
            # # --- B ---
            # # 4 dedos (índice, medio, anular, meñique) extendidos y juntos. Pulgar cruzado sobre la palma.
            # if not mensaje:
            #     if index_extended and middle_extended and ring_extended and pinky_extended and \
            #        distancia_euclidiana(index_finger_tip, middle_finger_tip) < 35 and \
            #        distancia_euclidiana(middle_finger_tip, ring_finger_tip) < 35 and \
            #        distancia_euclidiana(ring_finger_tip, pinky_tip) < 35 and \
            #        thumb_tip[1] > index_finger_mcp[1] and thumb_tip[0] > index_finger_mcp[0] and \
            #        distancia_euclidiana(thumb_tip, ring_finger_mcp) < 50 : # Pulgar cerca de la base del anular/medio
            #         mensaje = "B"
            
            # # --- C ---
            # # Mano en forma de C. Dedos curvados, pulgar también curvado.
            # # Las puntas de los dedos NO están tocando el pulgar directamente como en O.
            # # Hay una apertura mayor. Todos los dedos están flexionados (tip_y > pip_y)
            # if not mensaje:
            #     if index_finger_tip[1] > index_finger_pip[1] and \
            #        middle_finger_tip[1] > middle_finger_pip[1] and \
            #        ring_finger_tip[1] > ring_finger_pip[1] and \
            #        pinky_tip[1] > pinky_pip[1] and \
            #        thumb_tip[1] > thumb_pip[1] and \
            #        distancia_euclidiana(thumb_tip, pinky_tip) > 60 and \
            #        distancia_euclidiana(thumb_tip, index_finger_tip) < 100 and \
            #        thumb_tip[0] > index_finger_tip[0] and pinky_tip[0] > thumb_tip[0]: # Pulgar a la izquierda del meñique (mano der)
            #         mensaje = "C"
                    
            #  # --- D ---
            # # Dedo índice extendido hacia arriba. Resto de dedos y pulgar forman un círculo.
            # elif index_finger_tip[1] < index_finger_pip[1] \
            #     and middle_finger_tip[1] > middle_finger_pip[1] \
            #     and ring_finger_tip[1] > ring_finger_pip[1] \
            #     and pinky_tip[1] > pinky_pip[1] \
            #     and distancia_euclidiana(thumb_tip, middle_finger_tip) < 50 \
            #     and distancia_euclidiana(thumb_tip, ring_finger_tip) < 50:
            #     # Opcional: verificar que el meñique también esté cerca del pulgar si forma parte del círculo
            #     # and distancia_euclidiana(thumb_tip, pinky_tip) < 50:
            #     mensaje = "D"
            
            
            # # --- E ---
            # # Todos los dedos flexionados hacia la palma, yemas sobre la palma. Pulgar flexionado sobre los dedos.
            # # Todas las puntas de los dedos (index, middle, ring, pinky) deben estar muy por debajo de sus MCPs.
            # # El pulgar también flexionado y sobre ellos.
            # if not mensaje:
            #      if index_finger_tip[1] > index_finger_mcp[1] + 20 and \
            #         middle_finger_tip[1] > middle_finger_mcp[1] + 20 and \
            #         ring_finger_tip[1] > ring_finger_mcp[1] + 20 and \
            #         pinky_tip[1] > pinky_mcp[1] + 20 and \
            #         thumb_tip[1] > index_finger_pip[1] and \
            #         distancia_euclidiana(thumb_tip, middle_finger_pip) < 60: # Pulgar sobre los dedos medios
            #          mensaje = "E"
                     
            # # --- F ---
            # # Dedo índice y pulgar se tocan formando un círculo. Resto de dedos (medio, anular, meñique) EXTENDIDOS.
            # if not mensaje:
            #     if distancia_euclidiana(thumb_tip, index_finger_tip) < 30 and \
            #        middle_extended and ring_extended and pinky_extended and \
            #        distancia_euclidiana(middle_finger_tip, ring_finger_tip) < 40 and \
            #        distancia_euclidiana(ring_finger_tip, pinky_tip) < 40:
            #         mensaje = "F"         
                     
            # # --- G ---
            # # Dedo índice extendido horizontalmente. Pulgar paralelo y encima o al lado del índice. Resto cerrados.
            # # Requiere movimiento lateral. Esta es una pose estática.
            # if not mensaje:
            #     # Índice horizontal: tip_x < pip_x < mcp_x (o al revés) Y tip_y ~ pip_y ~ mcp_y
            #     index_horizontal = (abs(index_finger_tip[1] - index_finger_mcp[1]) < 30 and \
            #                         index_finger_tip[0] < index_finger_pip[0] - 15) # Izquierda para mano derecha
            #     thumb_parallel_index = (abs(thumb_tip[1] - index_finger_pip[1]) < 30 and \
            #                             thumb_tip[0] < index_finger_pip[0] - 5 and \
            #                             distancia_euclidiana(thumb_tip, index_finger_pip) < 50)
            #     if index_horizontal and thumb_parallel_index and \
            #        middle_flexed and ring_flexed and pinky_flexed:
            #         mensaje = "G"

            # # --- H ---
            # # Similar a U (índice y medio extendidos y juntos), pero la orientación de la mano puede ser más horizontal.
            # # O el pulgar en una posición diferente. Por ahora, la diferencia con U/V/R es sutil sin más contexto.
            # # Aquí, intento que el pulgar esté más al lado, no encima de los otros dedos cerrados.
            # if not mensaje:
            #      if index_extended and middle_extended and \
            #         distancia_euclidiana(index_finger_tip, middle_finger_tip) < 35 and \
            #         ring_flexed and pinky_flexed and \
            #         thumb_tip[1] > middle_finger_mcp[1] and thumb_tip[0] > middle_finger_mcp[0] + 10: # Pulgar más al lado
            #          mensaje = "H"
                     
            # # --- I ---
            # # Dedo meñique extendido verticalmente. Resto cerrados, pulgar sobre ellos.
            # elif pinky_tip[1] < pinky_pip[1] \
            #     and index_finger_tip[1] > index_finger_pip[1] \
            #     and middle_finger_tip[1] > middle_finger_pip[1] \
            #     and ring_finger_tip[1] > ring_finger_pip[1] \
            #     and thumb_tip[1] > index_finger_pip[1] and thumb_tip[0] > index_finger_pip[0]:
            #     mensaje = "I"
                     
                     
            #  # --- J --- (I con movimiento)
            # # Pose de I: Meñique extendido, resto cerrados, pulgar sobre ellos o al lado.
            # is_i_pose = (pinky_extended and
            #              index_flexed and middle_flexed and ring_flexed and
            #              thumb_tip[1] > index_finger_mcp[1] and # Pulgar no extendido hacia arriba
            #              distancia_euclidiana(thumb_tip, index_finger_mcp) < 80) # Pulgar cerca de dedos cerrados
            # if is_i_pose:
            #     current_message = "I"
            #     # global previous_pinky_tip_j # Si es necesario por el scope
            #     if previous_pinky_tip_j is not None:
            #         displacement_j = distancia_euclidiana(pinky_tip, previous_pinky_tip_j)
            #         # Para J, el movimiento es principalmente hacia abajo y luego curva
            #         # Esta es una simplificación, solo mira el desplazamiento
            #         if displacement_j > MOTION_THRESHOLD_J and pinky_tip[1] > previous_pinky_tip_j[1]: # Se movió hacia abajo
            #             current_message = "J"
            #     previous_pinky_tip_j = pinky_tip
            #     mensaje = current_message
            # else:
            #     previous_pinky_tip_j = None


            # # --- K ---
            # # Dedos índice y medio extendidos y separados (V). Pulgar entre ellos o tocando la palma cerca del índice.
            # # La diferencia con V es la posición del pulgar.
            # if not mensaje:
            #      if index_extended and middle_extended and \
            #         distancia_euclidiana(index_finger_tip, middle_finger_tip) > 40 and \
            #         ring_flexed and pinky_flexed and \
            #         ( (thumb_tip[0] > index_finger_mcp[0] and thumb_tip[0] < middle_finger_mcp[0] and \
            #            thumb_tip[1] > index_finger_mcp[1] and thumb_tip[1] < index_finger_mcp[1] + 40 ) or \
            #           distancia_euclidiana(thumb_tip, index_finger_pip) < 40): # Pulgar entre o tocando índice
            #          mensaje = "K"
                     
            # # --- L ---
            # # Dedo índice y pulgar extendidos formando una L. Resto CERRADOS.
            # # Índice extendido hacia arriba. Pulgar extendido horizontalmente.
            # if not mensaje:
            #     if index_extended and \
            #        (abs(thumb_tip[1] - thumb_mcp[1]) < 30 and thumb_tip[0] < thumb_mcp[0] - 20) and \
            #        middle_flexed and ring_flexed and pinky_flexed:
            #         mensaje = "L"         
            
            #  # --- M --- (Para evitar confusión con Y)
            # # Dedos índice, medio y anular flexionados sobre el pulgar (puntas hacia abajo). Meñique cerrado.
            # # Pulgar debajo de las bases de los 3 dedos y por encima de sus puntas.
            # if not mensaje:
            #     if index_finger_tip[1] > index_finger_mcp[1] and \
            #        middle_finger_tip[1] > middle_finger_mcp[1] and \
            #        ring_finger_tip[1] > ring_finger_mcp[1] and \
            #        pinky_flexed and \
            #        thumb_tip[1] < index_finger_mcp[1] and thumb_tip[1] > index_finger_tip[1] and \
            #        thumb_tip[0] > index_finger_mcp[0] and thumb_tip[0] < ring_finger_mcp[0] + 10:
            #         mensaje = "M"
            
            # # --- N ---
            # # Dedos índice y medio flexionados sobre el pulgar. Anular y meñique cerrados.
            # if not mensaje:
            #      if index_finger_tip[1] > index_finger_mcp[1] and \
            #         middle_finger_tip[1] > middle_finger_mcp[1] and \
            #         ring_flexed and pinky_flexed and \
            #         thumb_tip[1] < index_finger_mcp[1] and thumb_tip[1] > index_finger_tip[1] and \
            #         thumb_tip[0] > index_finger_mcp[0] and thumb_tip[0] < middle_finger_mcp[0] + 10:
            #          mensaje = "N"
                     
            # # --- Ñ --- (Pose estática: como N, pero con movimiento de muñeca)
            # elif index_finger_tip[1] > index_finger_mcp[1] \
            #     and middle_finger_tip[1] > middle_finger_mcp[1] \
            #     and ring_finger_tip[1] > ring_finger_pip[1] \
            #     and pinky_tip[1] > pinky_pip[1] \
            #     and thumb_tip[1] < index_finger_mcp[1] and thumb_tip[1] > index_finger_tip[1] \
            #     and thumb_tip[0] > index_finger_tip[0] and thumb_tip[0] < middle_finger_tip[0] \
            #     and True: # Necesita una forma de diferenciar de N si no hay movimiento. Momentáneamente igual a N.
            #     mensaje = "Ñ"         
                     
            # # --- O ---
            # # Todos los dedos forman un círculo con el pulgar.
            # # Las puntas de los dedos índice, medio, anular, meñique deben estar cerca entre sí Y cerca del pulgar.
            # # Todas las PIPs deben estar flexionadas.
            # if not mensaje:
            #     if distancia_euclidiana(thumb_tip, index_finger_tip) < 45 and \
            #        distancia_euclidiana(index_finger_tip, middle_finger_tip) < 45 and \
            #        distancia_euclidiana(middle_finger_tip, ring_finger_tip) < 45 and \
            #        distancia_euclidiana(ring_finger_tip, pinky_tip) < 45 and \
            #        distancia_euclidiana(pinky_tip, thumb_tip) < 60 and \
            #        index_finger_tip[1] > index_finger_pip[1] and \
            #        middle_finger_tip[1] > middle_finger_pip[1] and \
            #        ring_finger_tip[1] > ring_finger_pip[1] and \
            #        pinky_tip[1] > pinky_pip[1]:
            #         mensaje = "O"
                    
            # # --- P ---
            # # Mano hacia abajo. Índice y medio extendidos (como K invertida), pulgar entre índice y medio.
            # # Dedos principales apuntan hacia abajo: tip_y > pip_y > mcp_y
            # if not mensaje:
            #     index_down = index_finger_tip[1] > index_finger_pip[1] + 15 and index_finger_pip[1] > index_finger_mcp[1] + 10
            #     middle_down = middle_finger_tip[1] > middle_finger_pip[1] + 15 and middle_finger_pip[1] > middle_finger_mcp[1] + 10
            #     thumb_between_down = (thumb_tip[1] > index_finger_pip[1] and \
            #                           thumb_tip[0] > index_finger_pip[0] and thumb_tip[0] < middle_finger_pip[0])

            #     if index_down and middle_down and ring_flexed and pinky_flexed and thumb_between_down:
            #         mensaje = "P"
            
            # # --- Q --- (Para evitar confusión con F)
            # # Como G pero apuntando hacia abajo. Índice extendido hacia abajo, pulgar al lado, formando una pinza.
            # # Resto de dedos cerrados.
            # if not mensaje:
            #     if index_finger_tip[1] > index_finger_mcp[1] and abs(index_finger_tip[0] - index_finger_mcp[0]) < 30 and \
            #        thumb_tip[1] > thumb_mcp[1] and abs(thumb_tip[0] - thumb_mcp[0]) < 30 and \
            #        distancia_euclidiana(thumb_tip, index_finger_tip) < 50 and \
            #        middle_flexed and ring_flexed and pinky_flexed:
            #         mensaje = "Q"
            
            # # --- R --- (Para evitar confusión con H y V)
            # # Dedos índice y medio EXTENDIDOS y CRUZADOS. Resto cerrados.
            # if not mensaje:
            #     # Condición de cruce: la x de una punta está a un lado de la pip de la otra, y viceversa.
            #     # Y las puntas están cerca.
            #     crossed_condition_1 = (index_finger_tip[0] < middle_finger_pip[0] and middle_finger_tip[0] > index_finger_pip[0])
            #     crossed_condition_2 = (middle_finger_tip[0] < index_finger_pip[0] and index_finger_tip[0] > middle_finger_pip[0])
                
            #     if index_extended and middle_extended and \
            #        (crossed_condition_1 or crossed_condition_2) and \
            #        distancia_euclidiana(index_finger_tip, middle_finger_tip) < 50 and \
            #        ring_flexed and pinky_flexed and \
            #        distancia_euclidiana(thumb_tip, ring_finger_mcp) < 70:
            #         mensaje = "R"
            
            
            #  # --- S ---
            # # Puño cerrado, pulgar sobre los dedos índice y medio (cruzado en frente).
            # if not mensaje:
            #     if index_flexed and middle_flexed and ring_flexed and pinky_flexed and \
            #        thumb_tip[1] > index_finger_mcp[1] and thumb_tip[1] < index_finger_pip[1] -5 and \
            #        thumb_tip[0] > index_finger_pip[0] and thumb_tip[0] < ring_finger_pip[0]: # Pulgar encima
            #         mensaje = "S"
            
            # # --- T ---
            # # Puño cerrado, pulgar entre el índice y el medio (asomando la yema).
            # if not mensaje:
            #     if index_flexed and middle_flexed and ring_flexed and pinky_flexed and \
            #        thumb_tip[1] < index_finger_pip[1] and thumb_tip[1] > index_finger_tip[1] -5 and \
            #        thumb_tip[0] > index_finger_pip[0] and thumb_tip[0] < middle_finger_pip[0]:
            #         mensaje = "T"
            
            # # --- U ---
            # # Dedos índice y medio EXTENDIDOS y JUNTOS. Resto cerrados. Pulgar sobre ellos o al lado.
            # if not mensaje:
            #     if index_extended and middle_extended and \
            #        distancia_euclidiana(index_finger_tip, middle_finger_tip) < 35 and \
            #        ring_flexed and pinky_flexed and \
            #        distancia_euclidiana(thumb_tip, ring_finger_mcp) < 70:
            #         mensaje = "U"

            # # --- V --- (Para evitar confusión con U y H)
            # # Dedos índice y medio EXTENDIDOS y SEPARADOS. Resto cerrados. Pulgar sobre ellos o al lado.
            # if not mensaje:
            #     if index_extended and middle_extended and \
            #        distancia_euclidiana(index_finger_tip, middle_finger_tip) > 45 and \
            #        ring_flexed and pinky_flexed and \
            #        distancia_euclidiana(thumb_tip, ring_finger_mcp) < 70: # Similar al pulgar de U
            #         mensaje = "V"
            
            # # --- W ---
            # # Dedos índice, medio y anular extendidos y separados. Meñique cerrado, pulgar sobre él.
            # elif index_finger_tip[1] < index_finger_pip[1] \
            #     and middle_finger_tip[1] < middle_finger_pip[1] \
            #     and ring_finger_tip[1] < ring_finger_pip[1] \
            #     and pinky_tip[1] > pinky_pip[1] \
            #     and distancia_euclidiana(index_finger_tip, middle_finger_tip) > 30 \
            #     and distancia_euclidiana(middle_finger_tip, ring_finger_tip) > 30 \
            #     and thumb_tip[1] > pinky_pip[1]: # Pulgar sobre meñique
            #     mensaje = "W"
            
            # # --- X --- (Para evitar confusión con E)
            # # Dedo índice flexionado en forma de gancho. Resto CERRADOS.
            # # index_tip[1] > index_pip[1] pero index_pip[1] < index_mcp[1] (gancho)
            # if not mensaje:
            #     if index_finger_tip[1] > index_finger_pip[1] and index_finger_pip[1] < index_finger_mcp[1] and \
            #        middle_flexed and ring_flexed and pinky_flexed and \
            #        distancia_euclidiana(middle_finger_tip, wrist) < distancia_euclidiana(middle_finger_pip, wrist) and \
            #        distancia_euclidiana(thumb_tip, index_finger_mcp) < 60: # Pulgar cerca del índice
            #         mensaje = "X"

            # # --- Y ---
            # # Pulgar y meñique EXTENDIDOS. Resto (índice, medio, anular) CERRADOS.
            # if not mensaje:
            #     # Pulgar extendido (puede ser hacia arriba o lateral)
            #     thumb_is_extended_y = (thumb_tip[1] < thumb_pip[1] or \
            #                          (abs(thumb_tip[1] - thumb_mcp[1]) < 30 and thumb_tip[0] < thumb_mcp[0] - 20))

            #     if pinky_extended and thumb_is_extended_y and \
            #        index_flexed and middle_flexed and ring_flexed:
            #         mensaje = "Y"
            
            # # --- Z --- (Índice extendido con movimiento)
            # # Pose base Z: Índice extendido, resto cerrados, pulgar sobre ellos o al lado.
            # is_static_z_pose = (index_extended and
            #                     middle_flexed and ring_flexed and pinky_flexed and
            #                     thumb_tip[1] > middle_finger_mcp[1] and # Pulgar no extendido
            #                     distancia_euclidiana(thumb_tip, middle_finger_mcp) < 80)

            # if is_static_z_pose and not mensaje: # Solo si no es J/I
            #     current_message = "Z (estática)" # o "Índice arriba"
            #     # global previous_index_tip_z
            #     if previous_index_tip_z is not None:
            #         displacement_z = distancia_euclidiana(index_finger_tip, previous_index_tip_z)
            #         if displacement_z > MOTION_THRESHOLD_Z:
            #             current_message = "Z"
            #     previous_index_tip_z = index_finger_tip
            #     mensaje = current_message
            # elif not is_static_z_pose and not mensaje: # Si no es pose Z Y mensaje está vacío
            #     previous_index_tip_z = None