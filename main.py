from modules import ffmpeg_handler as fh
from modules import youtube_downloader as yd

broker = True

# Setting up Menu

while broker:

    option = input("""
        Terminal Menu - Subtitle generator
                   
1. Download Video from YouTube.
2. Create and insert Spanish to English subtitles from video.
0. closing the program. 
""")
    
    if option == "1":

        name = input("""
Name the video file (without extention, just the name): """)

        url = input("""
Enter the URL of the video to download: """)

        yd.download_youtube(url, name)

    elif option == "2":

        name = input("""
Enter the name of the video file: """)

        fh.extract_audio(name)
    
    elif option == "0":

        broker = False

    else:

        print("")
        print("Enter a correct value (0-2)")