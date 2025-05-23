import cv2
import mediapipe as mp
import time
import math 
import speech_recognition as sr
import threading
    
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
# MÉTODOS PARA SABER SI UN DEDO ESTÁ LEVANTADO (MANO VERTICAL)
# -----------------------------------------------------------------------------
# Asumimos:
# - La mano debe estar orientada verticalmente.
# - "Verticalmente" significa que la punta del dedo (TIP) esté más arriba que su articulación base (MCP)
# - Hay que tener en cuenta en la mayoría de las configuraciones de imagen, Y disminuye hacia arriba,
#   por lo tanto, cuanto más alto esté el punto más pequeña será su coordenada.
def pulgar_levantado_vertical(thumb_tip, thumb_ip, thumb_mcp, umbral_relativo_mcp=15, umbral_relativo_ip=5):
    return thumb_tip[1] < thumb_mcp[1] - umbral_relativo_mcp and \
            thumb_tip[1] < thumb_ip[1] - umbral_relativo_ip
        

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

# -----------------------------------------------------------------------------
# MÉTODO PARA SABER LA ORIENTACIÓN DE LA MANO
# -----------------------------------------------------------------------------

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
        - "BOCA_ABAJO" (si la muñeca está por encima del MCP)
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
    if abs_delta_x < epsilon or abs_delta_y / (abs_delta_x + epsilon) > ratio_threshold:
        if wrist_coords[1] < middle_finger_mcp_coords[1]:
            return "BOCA_ABAJO"
        else:
            return "VERTICAL"

    # Caso predominantemente HORIZONTAL
    # (abs_delta_x es significativamente mayor que abs_delta_y)
    # Evaluar orientación horizontal
    if abs_delta_y < epsilon or (abs_delta_x / abs_delta_y > ratio_threshold):
        if delta_x > 0:
            return "HORIZONTAL_DERECHA"
        else:
            return "HORIZONTAL_IZQUIERDA"

    # Si no es claramente vertical ni horizontal según el umbral
    return "DIAGONAL_INDETERMINADA"


# -----------------------------------------------------------------------------
# VARIABLES GLOBALES
# -----------------------------------------------------------------------------
# OpenRouter API 
openrouter_api_key = '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'

# Inicializamos el reconocimiento de voz y el micrófono
r = sr.Recognizer()
mic = sr.Microphone()

mensaje_mostrar = ""
mensaje_error = ""
escuchando = False # Creamos esta variable para evitar que el reconocimiento de voz se dispare múltiples veces

# -----------------------------------------------------------------------------
# MÉTODO PARA REALIZAR LA SÍNTESIS POR VOZ
# -----------------------------------------------------------------------------
def escuchar_y_transcribir():
    global mensaje_mostrar, mensaje_error, escuchando # Recogemos las variables de fuera de la función
    escuchando = True
    print("🔴 Escuchando...")
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=2)
            mensaje_mostrar = r.recognize_google(audio, language="es-ES").lower()
            print(f"👂 Transcrito: {mensaje_mostrar}")
            mensaje_error=""
        except sr.WaitTimeoutError:
            mensaje_error = "🔇 No se detectó audio."
        except sr.UnknownValueError:
            mensaje_error = "❓ No se ha podido reconocer."
        except sr.RequestError as e:
            mensaje_error = f"⚠️ Error en Google: {e}"
    escuchando = False # Lo ponemos a false para 

# -----------------------------------------------------------------------------
#                              INICIO DEL PROGRAMA
# -----------------------------------------------------------------------------
# Asociamos la cámara o dispositivo de captura a una variable
dispositivoCaptura = cv2.VideoCapture(0)

# Asignación para la detección de los puntos de la mano (visto en la imagen PuntosMano.png)
mpManos = mp.solutions.hands

# Creación de la instancia de detección de manos                                    (0.1 la minima 1 la maxima)precisión
#                     Con esto indicamos que    | Con esto indicamos | Con esto indicamos cuanta      | Con esto hacemos el trackeo 
#                     va a ser una camara o un  | el número máximo   | certeza tiene que tener de     | de las manos
#                     video (no imagen sola)    | de manos           | que es una mano para mostrarlo |
manos = mpManos.Hands(static_image_mode = False, max_num_hands = 1,   min_detection_confidence = 0.9,   min_tracking_confidence = 0.9)

# Esto sirve para poder dibujar dentro de nuestro cuadro de cámara 
mpDibujo = mp.solutions.drawing_utils

# Esto sirve para darle estilo al dibujo
mpDrawingStyles = mp.solutions.drawing_styles

COOLDOWN = 2.0     # segundos mínimos entre detecciones
ultimo_detection_time = 0.0
ultimo_tiempo = time.time()

previous_pinky_tip_j = None
previous_index_tip_z = None
MOTION_THRESHOLD_J = 10 # Ajustar
MOTION_THRESHOLD_Z = 15 # Ajustar

# Creo una variable para saber si quiere traducir de lengua de signos a texto o de voz a texto
modoSignAtexto = True
modoVozAtexto = False # not signAtexto
barraEspaciadora = False

# Ahora un while true para poder capturar los frames de la cámara todo el rato
while True:
    succes, img = dispositivoCaptura.read()


    img.flags.writeable = False
    # Pasamos la imagen capturada a rgb para que detecte bien las manos
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)# Convierte la imagen que detecta la cámara de BGR a RGB

    # Creamos una variable resultado que detecta si hay o si no hay manos
    resultado = manos.process(imgRGB)
    img.flags.writeable = True

    if modoSignAtexto:
        # 3) reseteo si no hay letras en 2 segundo
        if time.time() - ultimo_tiempo > 2.0:
            mensaje_mostrar = ""
        # Comprobamos si la mano detectada tiene varios landmarks (puntos de la mano de la imagen PuntosMano.png)
        if resultado.multi_hand_landmarks:
            # En caso de que si por cada landmark mostramos el punto
            for id, lm in enumerate(resultado.multi_hand_landmarks):
                mpDibujo.draw_landmarks(img, lm, mpManos.HAND_CONNECTIONS, mpDrawingStyles.get_default_hand_landmarks_style(), mpDrawingStyles.get_default_hand_connections_style()) # Captura la mano entera todo el rato
                alto, ancho, color = img.shape # Calculamos la posición en píxeles de la imagen
                    
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
                menique_extendidoHD = menique_extendido_horizontal_derecha(pinky_tip, pinky_pip, pinky_mcp)
                menique_extendidoHI = menique_extendido_horizontal_izquierda(pinky_tip, pinky_pip, pinky_mcp)
                menique_extendidoV = menique_levantado_vertical(pinky_tip, pinky_pip, pinky_mcp)
                # Pulgar
                pulgar_extendidoHD = pulgar_extendido_horizontal_derecha(thumb_tip, thumb_ip, thumb_mcp)
                pulgar_extendidoHI = pulgar_extendido_horizontal_izquierda(thumb_tip, thumb_ip, thumb_mcp)
                pulgar_extendidoV = pulgar_levantado_vertical(thumb_tip, thumb_ip, thumb_mcp)
            
                mensaje = ""
                orientacion = obtener_orientacion_mano(wrist, middle_mcp) # Obtenemos la orientación de la mano
                
                # Opciones de Letra para cada una de las orientaciones para ahorrar calculos al programa
                # ____________________________________________VERTICAL____________________________________________
                if orientacion=="VERTICAL":
                    # mensaje = "Ver"
                    if index_tip[1]>index_mcp[1] and middle_tip[1]>middle_mcp[1] and ring_tip[1]>ring_mcp[1] and pinky_tip[1]>pinky_mcp[1] and thumb_ip[1]>middle_mcp[1] and abs(thumb_ip[0]-middle_mcp[0])<15: # not indice_extendidoV and not corazon_extendidoV and not anular_extendidoV and not menique_extendidoV and thumb_tip[1]>middle_mcp[1] and not pulgar_extendidoV:
                        mensaje="A"
                    elif  index_tip[1]<index_mcp[1] and middle_tip[1]<middle_mcp[1] and ring_tip[1]<ring_mcp[1] and pinky_tip[1]<pinky_mcp[1] and 30 < abs(index_tip[1] - thumb_tip[1]) < 300 and abs(index_tip[0]-middle_tip[0])<20:
                        mensaje = "C"
                    elif indice_extendidoHD or indice_extendidoHI and abs(thumb_tip[0]-middle_tip[0])>5 or (corazon_extendidoHD or corazon_extendidoHI) and\
                        abs(thumb_tip[0]-pinky_tip[0])>15 or (menique_extendidoHD or menique_extendidoHI) and indice_extendidoV: 
                        mensaje = "D"
                    elif index_tip[1]>index_mcp[1] and middle_tip[1]>middle_mcp[1] and ring_tip[1]>ring_mcp[1] and pinky_tip[1]>pinky_mcp[1] and (pulgar_extendidoHD or pulgar_extendidoHI or pulgar_extendidoV) and abs(thumb_ip[0]-middle_mcp[0])>30:
                        mensaje = "E"
                    elif menique_extendidoV and corazon_extendidoV and anular_extendidoV and index_tip[1] > thumb_tip[1] and 10<(index_tip[1]-thumb_tip[1])<30:
                        mensaje="T"
                    elif not menique_extendidoV and not anular_extendidoV  and indice_extendidoV and corazon_extendidoV and 5 < abs(index_tip[0]-middle_tip[0]) > 40 and abs(pinky_mcp[0]-thumb_tip[0])>100:
                        mensaje = "H"
                    elif index_tip[1]>index_mcp[1] and middle_tip[1]>middle_mcp[1] and ring_tip[1]>ring_mcp[1] and menique_extendidoV and index_pip[1]<thumb_tip[1]:
                        mensaje="I"
                    elif indice_extendidoV and (pulgar_extendidoHD or pulgar_extendidoHI) and not menique_extendidoV and not anular_extendidoV and not corazon_extendidoV:
                        mensaje="L"
                    elif anular_extendidoV and corazon_extendidoV and 15 > abs(thumb_tip[1]-index_tip[1]) > 5 and not (pulgar_extendidoHD or pulgar_extendidoHI):
                        mensaje = "O"
                    elif indice_extendidoV and corazon_extendidoV and anular_extendidoV and not menique_extendidoV and abs(ring_tip[0]-index_tip[0]) < 50:
                        mensaje = "P"
                    elif menique_extendidoV and corazon_extendidoV and anular_extendidoV and indice_extendidoV and abs(thumb_tip[0]-index_tip[0]) < 40:
                        mensaje = "Q" # La letra Q está tanto en orientación vertical como indeterminada porque es una postura compleja
                    elif not menique_extendidoV and not anular_extendidoV and corazon_extendidoV and indice_extendidoV and abs(index_pip[1]-middle_pip[1])<15 and abs(index_pip[0]-middle_pip[0])<15: # Si el punto PIP del dedo Corazón está entre el pip y el dip del índice significa que los dedos están cruzados
                        mensaje = "R"
                    elif anular_extendidoV and corazon_extendidoV and (pulgar_extendidoHD or pulgar_extendidoHI) and 40 > abs(thumb_mcp[1]-index_tip[1]) > 5:
                        mensaje = "S"
                    elif pinky_tip[1]>pinky_mcp[1] and ring_tip[1]>ring_mcp[1] and index_tip[1]<index_mcp[1] and middle_tip[1]<middle_mcp[1] and 5 < abs(index_tip[0]-middle_tip[0]) > 30 and abs(ring_tip[0]-thumb_tip[0])<=10 and ring_dip[1]<thumb_tip[1]:
                        mensaje = "U"
                    elif index_tip[1]>index_mcp[1] and middle_tip[1]>middle_mcp[1] and ring_tip[1]>ring_mcp[1] and pinky_mcp[1]>pinky_tip[1]>pinky_dip[1]:
                        mensaje="Y" # Realmente es un gesto pero he decidido poner la que sería la ultima posición del gesto porque no puede reconocer movimiento
                    elif index_tip[1]>index_mcp[1] and middle_tip[1]>middle_mcp[1] and ring_tip[1]>ring_mcp[1] and menique_extendidoV and index_pip[1]>thumb_tip[1]:
                        mensaje="J" # Es igual que la I porque es poner la misma posición de la mano dada la vuelta y hacer un gesto de giro, por eso para diferenciarla le he puesto que el pulgar deba estar levantado también
                    elif indice_extendidoV and corazon_extendidoV and anular_extendidoV and not menique_extendidoV and abs(pinky_tip[0]-thumb_tip[0])>5 and abs(ring_tip[0]-index_tip[0]) >= 50:
                        mensaje = "W"
                    elif index_tip[1]<index_mcp[1] and pinky_mcp[1]<pinky_tip[1] and ring_mcp[1]<ring_pip[1] and middle_mcp[1]<thumb_tip[1]<middle_pip[1]:
                        mensaje = "K"
                    
                # ___________________________________________HORIZONTAL___________________________________________
                elif orientacion == "HORIZONTAL_DERECHA" or orientacion =="HORIZONTAL_IZQUIERDA":
                    # mensaje = "Hor"
                    if (menique_extendidoHD and anular_extendidoHD and corazon_extendidoHD and indice_extendidoHD) or (menique_extendidoHI and anular_extendidoHI and corazon_extendidoHI and indice_extendidoHI):
                        mensaje = "B"
                    elif (not menique_extendidoHD and not anular_extendidoHD and not corazon_extendidoHD and indice_extendidoHD) or (not menique_extendidoHI and not anular_extendidoHI and not corazon_extendidoHI and indice_extendidoHI):
                        mensaje = "G"
                    elif (not menique_extendidoHD and not anular_extendidoHD and not corazon_extendidoHD and abs(index_mcp[0]-index_tip[0])<30) or (not menique_extendidoHI and not anular_extendidoHI and not corazon_extendidoHI and abs(index_mcp[0]-index_tip[0])<30):
                        mensaje = "X"
                
                # ____________________________________________DIAGONAL____________________________________________
                elif orientacion == "DIAGONAL_INDETERMINADA":
                    # mensaje = "DI"
                    if menique_extendidoV and corazon_extendidoV and anular_extendidoV and indice_extendidoV and abs(pinky_tip[0]-index_tip[0]) <70:
                        mensaje = "Q" # La letra Q está tanto en orientación vertical como indeterminada porque es una postura compleja
                    elif not menique_extendidoV and not anular_extendidoV  and indice_extendidoV and corazon_extendidoV and 5 < abs(index_tip[0]-middle_tip[0]) > 40 and abs(pinky_mcp[0]-thumb_tip[0])>100:
                        mensaje = "H"
                    elif index_tip[1]>index_mcp[1] and middle_tip[1]>middle_mcp[1] and ring_tip[1]>ring_mcp[1] and menique_extendidoV:
                        mensaje="Z" # La Z es exactamente igual que la I porque se pinta el gesto con el meñique pero al pintarlo debes inclinar la mano, por eso no detecta el gesto pero si la posición
                    elif index_tip[1]<index_mcp[1] and pinky_mcp[1]<pinky_tip[1] and ring_mcp[1]<ring_pip[1] and middle_mcp[1]<thumb_tip[1]<middle_pip[1]:
                        mensaje = "K"
                    elif not menique_extendidoV and not anular_extendidoV  and index_tip[1]<index_mcp[1] and middle_tip[1]<middle_mcp[1] and 5 < abs(index_tip[0]-middle_tip[0]) > 30 and abs(ring_tip[0]-thumb_tip[0])<=5:
                        mensaje = "V"
                    elif (not menique_extendidoHD and not anular_extendidoHD and not corazon_extendidoHD and abs(index_mcp[0]-index_tip[0])<30) or (not menique_extendidoHI and not anular_extendidoHI and not corazon_extendidoHI and abs(index_mcp[0]-index_tip[0])<30):
                        mensaje = "X"
                        
                # ___________________________________________BOCA ABAJO___________________________________________
                elif orientacion == "BOCA_ABAJO":
                    # mensaje = "BA"
                    if index_tip[1]>index_mcp[1] and middle_tip[1]>middle_mcp[1] and ring_tip[1]>ring_mcp[1] and ring_tip[1]>middle_dip[1]:
                        mensaje = "M"
                    elif index_tip[1]>index_mcp[1] and middle_tip[1]>middle_mcp[1] and ring_tip[1]<middle_dip[1] and abs(thumb_tip[0]-index_pip[0])>16:
                        mensaje = "N" 
                    elif index_tip[1]>index_mcp[1] and middle_tip[1]>middle_mcp[1] and ring_tip[1]<middle_dip[1] and abs(thumb_tip[0]-index_pip[0])<=15:
                        mensaje = "Ñ"# Esta letra está mal porque realmente debe tratarse con movimiento pero al no poder se me ocurrió poner el pulgar cerca del índice para diferenciarla de la N
                
                # Comprobación del tiempo desde que se detectó la última letra
                now = time.time()
                if mensaje:
                    if now - ultimo_detection_time >= COOLDOWN: 
                        mensaje_mostrar += mensaje
                        ultimo_detection_time = now
                        ultimo_tiempo = time.time()
                
                # print(orientacion)
                
                # Mostramos la letra/buffer de letras o mensaje en caso de sintesis por voz
                cv2.putText(img, mensaje_mostrar, (0, 100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                2.0, (0, 0, 255), 4)

                # Mostramos la imagen
                cv2.imshow("Image", img)
                if cv2.waitKey(1) & 0xFF == 27:
                        break
                
    
    elif modoVozAtexto:
        if barraEspaciadora and not escuchando:
            threading.Thread(target=escuchar_y_transcribir, daemon = True).start() # Metemos el método escuchar_y_transcribir en un hilo para que no bloquee la cámara y que pueda escuchar en segundo plano
            ultimo_tiempo=time.time()
            barraEspaciadora = False # Volvemos a desactivarlo hasta que se pulse el espacio
        
        # Esperar a que haya algo que mostrar
        texto_final = mensaje_mostrar if mensaje_mostrar else mensaje_error
        # Mostrar el texto (solo si hay algo)
        if texto_final:
            cv2.putText(img, texto_final, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
        
        # Mostrar mensaje si ha pasado un tiempo sin hablar
        if time.time() - ultimo_tiempo > 6.0:
            mensaje_mostrar = ""
            mensaje_error = ""
        
        # Mostramos la imagen
        cv2.imshow("Cámara + voz", img)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27: # Interrumpimos el programa manualmente
            break
        elif key == 32: # Pulsamos barra espaciadora para empezar a escuchar
            barraEspaciadora = True
        elif key == ord('m') or key == ord('M'): # Si se presiona 'm' (minúscula) o 'M' (mayúscula)
            if modoSignAtexto:
                modoSignAtexto = False
                modoVozAtexto = True
            else:
                modoSignAtexto = True
                modoVozAtexto = False

dispositivoCaptura.release()
cv2.destroyAllWindows()
