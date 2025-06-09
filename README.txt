---

# Traductor de Lengua de Signos (LSE) y Voz a Texto

Un proyecto de visión por computadora y reconocimiento de voz que traduce gestos del abecedario de la Lengua de Signos Española (LSE) y transcribe audio a texto en tiempo real.

## 📝 Descripción

Este proyecto presenta una aplicación multifuncional que utiliza la cámara y el micrófono de un ordenador para facilitar la comunicación a través de dos modos principales:

1.  **Traducción de Signos a Texto**: Interpreta en tiempo real los gestos de la mano correspondientes a las letras del abecedario de la LSE y los muestra como texto en pantalla.
2.  **Transcripción de Voz a Texto**: Captura audio a través del micrófono y lo convierte en texto.

La aplicación permite al usuario alternar entre estos dos modos de forma fluida con solo pulsar una tecla.

## ✨ Características

* **Reconocimiento de LSE en tiempo real**: Utiliza la librería MediaPipe para detectar los puntos de referencia de la mano y un sistema de reglas para clasificar las letras.
* **Transcripción de Voz**: Integra la librería `SpeechRecognition` para realizar la conversión de voz a texto en español.
* **Interfaz Visual Interactiva**: Muestra la señal de vídeo de la cámara, superponiendo el esqueleto de la mano detectada para proporcionar feedback visual al usuario.
* **Modo Dual**: Permite cambiar fácilmente entre el modo de reconocimiento de signos y el de voz.

## 🛠️ Requisitos e Instalación

Para ejecutar este proyecto, necesitas Python 3 y las siguientes librerías.

* `opencv-python`
* `mediapipe`
* `speechrecognition`
* `pyaudio`

Puedes instalar todas las dependencias ejecutando el siguiente comando en tu terminal:

```bash
pip install opencv-python mediapipe SpeechRecognition pyaudio
```

## 🚀 Uso y Controles

1.  **Ejecutar la aplicación**:
    Abre una terminal, navega hasta el directorio del proyecto y ejecuta:
    ```bash
    python pruebaDetectarManos_app.py
    ```
2.  **Controles del Programa**:
    * `'m'` / `'M'`: Pulsa la tecla 'm' para **alternar** entre el modo "Signos a Texto" y "Voz a Texto".
    * `Barra Espaciadora`: En el modo "Voz a Texto", púlsala para **iniciar la escucha**.
    * `Esc`: Pulsa la tecla 'Escape' para **cerrar la aplicación**.

## 📂 Estructura del Proyecto

* `pruebaDetectarManos_app.py`: El script principal que ejecuta la aplicación. Gestiona la captura de vídeo, la interfaz de usuario y la lógica de los modos.
* `entrenamiento.py`: Contiene la lógica de decisión (`letra_leida`) para identificar qué letra del LSE se está representando según la geometría de la mano.
* `calculoDeDistancias.py`: Módulo con funciones de ayuda para calcular distancias, determinar la orientación de la mano y el estado de los dedos.
* `pruebamicros.py`: Un script de utilidad para listar los micrófonos disponibles en tu sistema y sus correspondientes índices.

## 🎤 Configuración del Micrófono

Si el reconocimiento de voz no funciona, puede que esté utilizando el dispositivo de entrada incorrecto. Sigue estos pasos para solucionarlo:

1.  Ejecuta el script `pruebamicros.py` para ver una lista de tus micrófonos y sus índices de dispositivo.
    ```bash
    python pruebamicros.py
    ```
2.  El resultado será algo como: `1: Micrófono Externo (2 canales)`. Anota el número (índice) de tu micrófono.

3.  Abre el fichero `pruebaDetectarManos_app.py` en un editor.

4.  Localiza la línea donde se inicializa el micrófono (aproximadamente la línea 32).
    ```python
    mic = sr.Microphone()
    ```
5.  Modifícala para añadir el `device_index` que anotaste. Por ejemplo, si tu micrófono es el dispositivo 1:
    ```python
    mic = sr.Microphone(device_index=1)
    ```
6.  Guarda los cambios y vuelve a ejecutar la aplicación. El reconocimiento de voz ahora debería utilizar el micrófono correcto.