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

def letra_leida(thumb_tip,
index_tip,
middle_tip,
ring_tip,
pinky_tip,
thumb_ip,
index_pip,
middle_pip,
ring_pip,
pinky_pip,
index_dip,
middle_dip,
ring_dip,
pinky_dip,
thumb_mcp,
index_mcp,
middle_mcp,
ring_mcp,
pinky_mcp,
indice_extendidoHD,
indice_extendidoHI,
indice_extendidoV,
corazon_extendidoHD,
corazon_extendidoHI,
corazon_extendidoV,
anular_extendidoHD,
anular_extendidoHI,
anular_extendidoV,
menique_extendidoHD,
menique_extendidoHI,
menique_extendidoV,
pulgar_extendidoHD,
pulgar_extendidoHI,
pulgar_extendidoV,
orientacion):
    mensaje = ""
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
                
    return mensaje