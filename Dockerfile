# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias del sistema necesarias para OpenCV, PyAudio y herramientas de compilación
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    portaudio19-dev \
    gcc \
    python3-dev \
    && apt-get clean

# Instala las dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto si es necesario
EXPOSE 5000

# Comando para ejecutar el programa principal
CMD ["python", "pruebaDetectarManos_app.py"]