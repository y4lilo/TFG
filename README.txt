======================================================================
        Traductor de Lengua de Signos (LSE) y Voz a Texto
======================================================================

DESCRIPCIÓN
----------------------------------------------------------------------
Este proyecto es una aplicación en tiempo real que utiliza la cámara de un ordenador para dos funciones principales:
1.  Traducir gestos del abecedario de la Lengua de Signos Española (LSE) a texto.
2.  Transcribir el lenguaje hablado en español a texto mediante el micrófono.

La aplicación permite alternar entre estos dos modos de funcionamiento de forma sencilla.


CARACTERÍSTICAS
----------------------------------------------------------------------
- **Reconocimiento de LSE**: Detecta una mano a través de la cámara, analiza la posición de los dedos y la orientación de la mano para identificar letras del abecedario LSE.
- **Transcripción de Voz**: En el modo de voz, puede escuchar a través del micrófono y transcribir lo que se dice a texto.
- **Interfaz Visual**: Muestra la imagen de la cámara en tiempo real, dibujando los puntos de referencia (landmarks) de la mano detectada para dar feedback visual.
- **Doble Modo**: Permite cambiar fácilmente entre el modo de reconocimiento de signos y el de voz.


REQUISITOS
----------------------------------------------------------------------
Para ejecutar este proyecto, necesitas tener Python 3 instalado, junto con las siguientes librerías:

- opencv-python
- mediapipe
- speechrecognition
- pyaudio


INSTALACIÓN
----------------------------------------------------------------------
Puedes instalar todas las dependencias ejecutando el siguiente comando en tu terminal:

pip install opencv-python mediapipe SpeechRecognition pyaudio

IMPORTANTE
La instalación de mediapipe es que solo es
compatible oficialmente con las siguientes versiones de Python:
- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10

NO es compatible oficialmente con:
- Python 3.6 o anteriores (obsoleto)
- Python 3.11 o 3.12 (puede que funcione parcialmente, pero no está oficialmente
soportado y pueden fallar ciertas dependencias o binarios precompilados)


USO Y CONTROLES
----------------------------------------------------------------------
1.  **Ejecutar la aplicación**:
    Abre una terminal, navega hasta el directorio del proyecto y ejecuta el siguiente comando:
    
    python pruebaDetectarManos_app.py

2.  **Controles del programa**:
    - **Pulsar 'm' o 'M'**: Alterna entre el modo "Signos a Texto" y "Voz a Texto".
    - **Pulsar la Barra Espaciadora**: En el modo "Voz a Texto", pulsa esta tecla para que la aplicación comience a escuchar.
    - **Pulsar 'Esc'**: Cierra la aplicación en cualquier momento.


ESTRUCTURA DEL PROYECTO
----------------------------------------------------------------------
- **pruebaDetectarManos_app.py**: Es el fichero principal que ejecuta la aplicación. Gestiona la captura de vídeo, la interfaz de usuario y la lógica de los modos.
- **entrenamiento.py**: Contiene la lógica de decisión para identificar qué letra del LSE se está representando según la geometría de la mano.
- **calculoDeDistancias.py**: Módulo con funciones de ayuda para calcular distancias, determinar la orientación de la mano y el estado de los dedos (extendidos/doblados).
- **pruebamicros.py**: Un script de utilidad para listar los micrófonos disponibles en tu sistema y sus correspondientes índices.


CONFIGURACIÓN DEL MICRÓFONO
----------------------------------------------------------------------
Si el modo de reconocimiento de voz no funciona o no detecta audio, es posible que la aplicación no esté utilizando el micrófono correcto. Para solucionarlo:

1.  Ejecuta el script `pruebamicros.py`:
    
    python pruebamicros.py

2.  Este comando te mostrará una lista de los dispositivos de entrada de audio y su índice numérico (por ejemplo, `0: Micrófono Interno`, `1: Micrófono USB`).

3.  Abre el fichero `pruebaDetectarManos_app.py` con un editor de texto.

4.  Busca la línea (aproximadamente la línea 32):
    
    mic = sr.Microphone()

5.  Modifícala para incluir el índice de tu micrófono. Por ejemplo, si tu micrófono es el dispositivo 1:
    
    mic = sr.Microphone(device_index=1)

6.  Guarda el fichero y vuelve a ejecutar la aplicación.