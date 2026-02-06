import whisper as w
import os
import torch

# Generating Spanish subtitles of the temporal audio with Whisper

def generate_spanish_subtitles(audio_name):

    if not (os.path.exists(f"temp_{audio_name}_audio.wav")):

        print()
        print("Video not found")
        input()
        
        return None

    # If GPU is available, whisper uses it. Otherwise CPU is used

    if torch.cuda.is_available():
        
        device = "cuda"

    else:

        device = "cpu"

        print("GPU not available, using CPU (slower)")



    # Load small model 

    model = w.load_model("small").to(device)

    # Subtitle settings and running

    try:

        subtitles = model.transcribe(

            f"temp_{audio_name}_audio.wav",

            language = "es",
            task = "transcribe",
            fp16 = True if device == "cuda" else False,
            word_timestamps = True,
            best_of = 2,
            no_speech_threshold = 0.4,
            compression_ratio_threshold = 1.8,
            condition_on_previous_text = False,

        )

        return subtitles

    except Exception as ae:

        print()
        print(f"❌ Error: {type(ae).__name__}: {ae}")
        input()

        return None

    finally:
        
        # Deleting temporal audio

        if os.path.exists(f"temp_{audio_name}_audio.wav"):
           
            os.remove(f"temp_{audio_name}_audio.wav")

        # Emptying VRAM space

        del model

        if device == "cuda":

            torch.cuda.empty_cache()
