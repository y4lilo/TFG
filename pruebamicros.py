import speech_recognition as sr
import pyaudio

def listar_dispositivos_validos():
    p = pyaudio.PyAudio()
    print("Dispositivos de entrada válidos:\n")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"{i}: {info['name']} ({info['maxInputChannels']} canales)")
    p.terminate()

listar_dispositivos_validos()