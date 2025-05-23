
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