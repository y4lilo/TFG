import math

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
    
    # threading.Thread(target=audio_a_letra(mensaje), daemon = True).start()            
    return mensaje