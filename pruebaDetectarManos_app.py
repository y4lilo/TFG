import cv2
import mediapipe as mp
import time
import speech_recognition as sr
import threading
import calculoDeDistancias as cdd
import entrenamiento
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

# MÉTODO PARA REALIZAR LA SÍNTESIS POR VOZ 
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
                indice_extendidoHD = cdd.indice_extendido_horizontal_derecha(index_tip, index_pip, index_mcp)
                indice_extendidoHI = cdd.indice_extendido_horizontal_izquierda(index_tip, index_pip, index_mcp)
                indice_extendidoV = cdd.indice_levantado_vertical(index_tip, index_pip, index_mcp)
                # Medio
                corazon_extendidoHD = cdd.medio_extendido_horizontal_derecha(middle_tip, middle_pip, middle_mcp)
                corazon_extendidoHI = cdd.medio_extendido_horizontal_izquierda(middle_tip, middle_pip, middle_mcp)
                corazon_extendidoV = cdd.medio_levantado_vertical(middle_tip, middle_pip, middle_mcp)
                # Anular
                anular_extendidoHD = cdd.anular_extendido_horizontal_derecha(ring_tip, ring_pip, ring_mcp)
                anular_extendidoHI = cdd.anular_extendido_horizontal_izquierda(ring_tip, ring_pip, ring_mcp)
                anular_extendidoV = cdd.anular_levantado_vertical(ring_tip, ring_pip, ring_mcp)
                # Meñique
                menique_extendidoHD = cdd.menique_extendido_horizontal_derecha(pinky_tip, pinky_pip, pinky_mcp)
                menique_extendidoHI = cdd.menique_extendido_horizontal_izquierda(pinky_tip, pinky_pip, pinky_mcp)
                menique_extendidoV = cdd.menique_levantado_vertical(pinky_tip, pinky_pip, pinky_mcp)
                # Pulgar
                pulgar_extendidoHD = cdd.pulgar_extendido_horizontal_derecha(thumb_tip, thumb_ip, thumb_mcp)
                pulgar_extendidoHI = cdd.pulgar_extendido_horizontal_izquierda(thumb_tip, thumb_ip, thumb_mcp)
                pulgar_extendidoV = cdd.pulgar_levantado_vertical(thumb_tip, thumb_ip, thumb_mcp)
            
                mensaje = ""
                orientacion = cdd.obtener_orientacion_mano(wrist, middle_mcp) # Obtenemos la orientación de la mano
                
                
                mensaje = entrenamiento.letra_leida(thumb_tip, index_tip, middle_tip,ring_tip, pinky_tip,
                                          thumb_ip, index_pip, middle_pip, ring_pip, pinky_pip,
                                          index_dip, middle_dip, ring_dip, pinky_dip,
                                          thumb_mcp, index_mcp, middle_mcp, ring_mcp, pinky_mcp,
                                          indice_extendidoHD, indice_extendidoHI, indice_extendidoV,
                                          corazon_extendidoHD, corazon_extendidoHI, corazon_extendidoV,
                                          anular_extendidoHD, anular_extendidoHI, anular_extendidoV,
                                          menique_extendidoHD, menique_extendidoHI, menique_extendidoV,
                                          pulgar_extendidoHD, pulgar_extendidoHI, pulgar_extendidoV,
                                          orientacion)
                
                # Comprobación del tiempo desde que se detectó la última letra
                now = time.time()
                if mensaje:
                    if now - ultimo_detection_time >= COOLDOWN: 
                        mensaje_mostrar += mensaje
                        ultimo_detection_time = now
                        ultimo_tiempo = time.time()
                    # 3) reseteo si no hay letras en 2 segundo
                    if time.time() - ultimo_tiempo > 2.0:
                        mensaje_mostrar = ""
                
                # print(orientacion)
                # print(mensaje_mostrar)
                # Mostramos la letra/buffer de letras o mensaje en caso de sintesis por voz
                cv2.putText(img, mensaje_mostrar, (50, 50), 
                                cv2.FONT_HERSHEY_TRIPLEX, 
                                2.0, (255, 255, 255), 5)
                

                
    
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
