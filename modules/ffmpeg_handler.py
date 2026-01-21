import os
import subprocess
import sys

# Extrae audio de video

def extract_audio(video_name):

    # verificando que el archivo existe

    if not (os.path.exists(f"videos/{video_name}.mp4")):

        print("❌ Video no encontrado")
        return None

    try:

    # corre el comando "ffmpeg -i "video.mp4" -vn -ar 16000 -ac 1 "audio.wav" en CMD 

        subprocess.run([

            "ffmpeg",
            "-i", f"videos/{video_name}.mp4",
            "-vn", 
            "-ar", "16000", 
            "-ac", "1",
            "-af", "volume=1.2", 
            f"temp_{video_name}_audio.wav"

 # Deja ver todo en la terminal y permite que Python pueda lanzar exception si ffmpeg falla

], check = True, stdout = sys.stdout, stderr = sys.stderr) 
        
        print(f"✅ Audio extraído: temp_{video_name}_audio.wav") # Confirmacion
        
    # En caso de cualquier error, notifica cual es el error y finaliza funcion.

    except Exception as ae:

        print(f"❌ Error inesperado: {type(ae).__name__}: {ae}")
        return None