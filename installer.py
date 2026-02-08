# This script verifies if programs needed to run are installed or not.
# If they are not it installs them (Just working in windows 10+ for now)

import sys
import subprocess
import platform
import ctypes

def Chocolatey_Install():

    # Checking Chocolatey

    try:
        
        print("Checking if Chocolatey is installed")
        print()
        
        check = subprocess.run(
            
        ["choco", "-v"], 
        capture_output = True, 
        text = True, 
        timeout = 5
        
        ) 
        
        if check.returncode == 0:
       
            print("Chocolatey already installed")
            print((check.stdout.split('\n'))[0])
            print()
            
        else:
                    
            error = check.stdout[:300] if check.stdout else "unknown error"
                    
            print(f"Chocolatey could not be installed. Error: {error}...")
            print()
        
    except FileNotFoundError:
        
        # Installing Chocolatey with winget
        
            print("Installing Chocolatey")
        
            try:
            
                chocolatey = subprocess.run(
                
                    ["winget", "install", "-e", "--id", "Chocolatey.Chocolatey"],
                    capture_output = True,
                    text = True,
                    timeout = 900,
                )
                
                if chocolatey.returncode == 0:
                    
                    print("Chocolatey installed successfully")
                    
                    check = subprocess.run(
            
                        ["where", "choco"], 
                        capture_output = True, 
                        text = True, 
                        timeout = 5
                        
                        )
            
                    if check.returncode == 0:
                
                        print((check.stdout.split('\n'))[0])
                        print()
                    
                else:
                    
                    error = chocolatey.stdout[:300] if chocolatey.stdout else "unknown error"
                    
                    print(f"Chocolatey could not be installed. Error: {error}...")
                    print()
                
            except Exception as ae:
                
                    print()
                    print(f"❌ Error: {type(ae).__name__}: {ae}")
                    print("Press Enter to exit...")
                    input()
        
    except Exception as ae:
        
        print()
        print(f"❌ Error: {type(ae).__name__}: {ae}")
        print("Press Enter to exit...")
        input()

# Give admin permises to the script

def admin_permises():

    is_admin = False
    
    try:
        
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    
    except:
        
        is_admin = False
        
    if not is_admin:
        
        print("Program needs to be run as administrator")
        print("Re-starting as an administrator")
        print()
        
        install_path = f'"{sys.executable}"'
        safe_args = " ".join(([f'"{arg}"' for arg in sys.argv]))
        
        check = ctypes.windll.shell32.ShellExecuteW(
            
            None,                 
            "runas",              
            install_path,       
            safe_args,   
            None,                 
            1                     
        )
        
        if check <= 32:
            
            print("Failed to get administrator privileges.")
            print("Please run this script as Administrator.")
            print("Press Enter to exit...")
            input()
            
            sys.exit(1)
        
        sys.exit(0)
        
    print("Executing as administrator")
    print()
        

def py_compatible_v_finder():
    
    c = 0
    compatible_py = ""
    
    print("Looking for a compatible version of Python...")
    
    # Looking for other compatible versions of python than the one currently running
    
    while c > -4:
        
        try: 
            
            version = subprocess.run(
                
                
                ["py", f"3.{c+11}", "--version"],
                capture_output = True,
                text = True,
                timeout = 5
                
            )
            
            if version.returncode == 0:
                
                print(f"Python Version 3.{c+11} was found")
                
                compatible_py = f"py_version: 3.{c+11}"
                            
                return compatible_py
                
            else:
                
                print(f"Python Version 3.{c+11} was not found")
                
            c = c - 1
                
        except Exception as ae:
            
            print()
            print(f"❌ Error: {type(ae).__name__}: {ae}")
            print("Press Enter to exit...")
            input()
    
    return compatible_py

# Detects the GPU in the computer

def gpu_detecter():
    
    # Identiry the OS of the computer
    
    system = platform.system()
    
    print("Looking for GPUs")
    
    if system == "Windows":
        
        try:
            
            # If it is windows, it runs a cmd check
            
            gpu = subprocess.run(
                
                ["wmic", "path", "win32_VideoController", "get", "name"],
                capture_output = True,
                text = True,
                timeout = 20
                
                )
            
            # Runs if command goes well
            
            if gpu.returncode == 0:
                
               lines = gpu.stdout.split("\n")
               lines.remove(lines[0])

               GPUs = []
               
               # Get the GPU names
               
               for line in lines:
               
                    if line != "":
                       
                        line = line.strip()
                        line = line.upper()
                        
                        GPUs.append(line)
                        
                        print(f"GPU: {line} Found")
            
                # Read names and gets the best GPU
            
               for GPU in GPUs:
                    
                    if "NVIDIA" in GPU and ("GEFORCE" in GPU or "QUADRO" in GPU or "TESLA" in GPU ):
                        
                        print(f"The {GPU} will be used")
                        print()
                    
                        return "nvidia"
                    
                    elif ("AMD" in GPU or "RADEON" in GPU) and not ("VEGA" in GPU and not ("RX" in GPU)) and not ("GRAPHICS" in GPU):
                    
                        print(f"The {GPU} will be used")
                        print()    
                            
                        return "amd"
                        
               print("GPUs were not found. Using CPU therefore.")
               print()
                                
               return "cpu"
                                
        except Exception as ae:
    
            print()
            print(f"❌ Error: {type(ae).__name__}: {ae}")
            print("Press Enter to exit...")
            input()
            
    else:
        
        print(f"This system is {system}. The program is just available for windows atm")
        print()

print()
print("Starting Installer...")
print()

admin_permises()

# Checks that the current python running the program is a compatible version

print("Python Check")

print(f"Python version is: {sys.version}")

if (sys.version_info.major == 3) and (8 <= sys.version_info.minor <= 11):

    print("Current Python is compatible")
    print()
    
else: 
    
    print("Current Python is not compatible")
    
    compatible_py = py_compatible_v_finder()    
        
    if compatible_py == "":
        
        print()
        print("Python versions installed are incompatible")
        print()
        
        # Installing compatible python (3.11.9)
        
        try:
                        
            Chocolatey_Install()
            
            print("Installing compatible Python")
            print()
            
            py_get = subprocess.run(
            
                ["choco", "install", "python311", "--version=3.11.9", "-y"],
                capture_output = True,
                text = True,
                timeout = 300,
            
            )
            
            # Checking it was properly installed
            
            if py_get.returncode == 0:
                
                compatible_py = py_compatible_v_finder()
                
                if compatible_py != "":
                
                    print("Compatible Python Installed Successfully")
                    print(compatible_py)
                    print()
                    
                    # Running the script again with compatible version of python
                    
                    try:
            
                        re_run = subprocess.run(
                            
                        ["py", f"-{(compatible_py.split(' '))[1]}", "installer.py"],
                        capture_output = True,
                        text = True,
                        timeout = 1200   
                            
                        )
                        
                        sys.exit(re_run.returncode)
                        
                    except Exception as ae:
                        
                        print()
                        print(f"❌ Error: {type(ae).__name__}: {ae}")
                        print("Press Enter to exit...")
                        input()
                
            else:
                
                error = py_get.stdout[:300] if py_get.stdout else "unknown error"
                
                print(f"Compatible Python could not be Installed. Error: {error}...")
                print()
        
        
        except Exception as ae:
            
            print()
            print(f"❌ Error: {type(ae).__name__}: {ae}")
            print("Press Enter to exit...")
            input()

    else:
        
        try:
            
            re_run = subprocess.run(
                
            ["py", f"-{(compatible_py.split(' '))[1]}", "installer.py"],
            capture_output = True,
            text = True,
            timeout = 1200   
                
            )
            
            sys.exit(re_run.returncode)
            
        except Exception as ae:
            
            print()
            print(f"❌ Error: {type(ae).__name__}: {ae}")
            print("Press Enter to exit...")
            input()
    
# Checks if ffmpeg is already installed
    
try:
    
    print("FFmpeg Check")
    
    check = subprocess.run(
        
    ["ffmpeg", "-version"], 
    capture_output = True, 
    text = True, 
    timeout = 5
    ) 
    
    if check.returncode == 0:
        
        print("FFmpeg already installed")
        print((check.stdout.split('\n'))[0])
        print()
    
except FileNotFoundError:
    
    print("FFmpeg not installed")
    print()
    
    # Installing ffmpeg with winget
    
    print("Installing FFmpeg")
    print()
    
    try:
    
        ffmpeg = subprocess.run(
        
            ["winget", "install", "ffmpeg"],
            capture_output = True,
            text = True,
            timeout = 300,
        )
        
        if ffmpeg.returncode == 0:
            
            print("ffmpeg installed successfully")
            
            check = subprocess.run(
        
                ["ffmpeg", "-version"], 
                capture_output = True, 
                text = True, 
                timeout = 5
                
                )
    
            if "ffmpeg version" in check.stdout:
        
                print((check.stdout.split('\n'))[0])
                print()
            
        else:
            
            error = ffmpeg.stdout[:300] if ffmpeg.stdout else "unknown error"
            
            print(f"ffmpeg could not be installed. Error: {error}...")
            print()
        
    except Exception as ae:
        
            print()
            print(f"❌ Error: {type(ae).__name__}: {ae}")
            print("Press Enter to exit...")
            input()
    
except Exception as ae:
    
    print()
    print(f"❌ Error: {type(ae).__name__}: {ae}")
    print("Press Enter to exit...")
    input()
    
# yt-dlp check

print("Yt-dlp Check")

try:
    
    import yt_dlp
        
    print("Yt-dlp already installed")
    print(yt_dlp.version.__version__)
    print()
    
except ImportError:
    
    print("Yt-dlp not installed")
    print()
    
    # Installing yt-dlp with winget
    
    print("Installing Yt-dlp")
    print()
    
    try:
    
        check = subprocess.run(
        
            [sys.executable, "-m", "pip", "install", "yt-dlp"],
            capture_output = True,
            text = True,
            timeout = 300,
        )
        
        if check.returncode == 0:
            
            print("Yt-dlp installed successfully")
            
            import yt_dlp
            
            print(yt_dlp.version.__version__)
            print()
            
        else:
            
            error = check.stdout[:300] if check.stdout else "unknown error"
            
            print(f"Yt-dlp could not be installed. Error: {error}...")
            print()
            
    except Exception as ae:
    
        print()
        print(f"❌ Error: {type(ae).__name__}: {ae}")
        print("Press Enter to exit...")
        input()

# Checking Whisper 

print("Whisper Check")

try:
    
    import whisper 
    
    print("Whisper installed")
    print(f"version: {whisper.__version__}")
    print()
    
except ImportError:
    
    print("Whisper not installed")
    print()
    
    print("Installing Whisper")
    print()
    
    try:
    
        whispe = subprocess.run(
        
            [sys.executable, "-m", "pip", "install", "openai-whisper"],
            capture_output = True,
            text = True,
            timeout = 300,
        )
        
        if whispe.returncode == 0:
            
            print("whisper installed successfully")
            
            import whisper
            
            print(whisper.__version__)
            print()
            
        else:
            
            error = whispe.stdout[:300] if whispe.stdout else "unknown error"
            
            print(f"whisper could not be installed. Error: {error}...")
            print()
        
    except Exception as ae:
        
            print()
            print(f"❌ Error: {type(ae).__name__}: {ae}")
            print("Press Enter to exit...")
            input()

# Checking GPUs

gpu = gpu_detecter()

# Installing AI Drivers for selected GPU

if gpu == "nvidia":

    try:
    
        import torch 
    
        print(f"Torch already Installed")
        print(torch.__version__)
    
        if torch.cuda.is_available():
        
            gpu_name = torch.cuda.get_device_name()
        
            print(f"Nvidia GPU available: {gpu_name}")
            print()
        
        else: 
        
            print("Not Nvidia GPU available")
            print("Try updating Nvidia drivers")
            print()
        
    except ImportError:
    
        print("Torch not installed")
        print()
        
        print("Installing Torch for Nvidia")
        print()
        
        try:
            
            check = subprocess.run(
                
                [sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu118"],
                capture_output = True,
                text = True,
                timeout = 1200

            )
            
            if check.returncode == 0:
                
                import torch 
    
                print(f"Torch for Nvidia GPU Installed")    
                print(torch.__version__)
            
                if torch.cuda.is_available():
                
                    gpu_name = torch.cuda.get_device_name() 
                
                    print(f"Nvidia GPU available: {gpu_name}")
                    print()
                
                else: 
                
                    print("Not Nvidia GPU available")
                    print("Try updating Nvidia drivers")
                    print()
                    
            else:
            
                error = check.stdout[:300] if check.stdout else "unknown error"
                
                print(f"Torch for Nvidia GPU could not be installed. Error: {error}...")
                print()
                    
        except Exception as ae:
    
            print()
            print(f"❌ Error: {type(ae).__name__}: {ae}")
            print("Press Enter to exit...")
            input()

    except Exception as ae:
    
        print()
        print(f"❌ Error: {type(ae).__name__}: {ae}")
        print("Press Enter to exit...")
        input()
        
elif gpu == "amd":
    
    try:
    
        import directml
        
        print("Torch DirecTML (amd) already installed")
        print(directml.__version__)
        print()
        
    except ImportError:
        
        print("Torch not installed")
        print()
        
        print("Installing Torch for AMD (DirecTML)")
        print()
        
        try:
            
            check = subprocess.run(
                
                [sys.executable, "-m", "pip", "install", "torch-directml"],
                capture_output=True,
                text=True,
                timeout=1200 
                
            )
            
            if check.returncode == 0:
                
                print("Torch DirecTML (amd) successfully installed")
                
                import directml
                
                print(directml.__version__)
                print()
                
            else:
            
                error = check.stdout[:300] if check.stdout else "unknown error"
                
                print(f"Torch DirecTML (amd) could not be installed. Error: {error}...")
                print()
            
        except Exception as ae:
        
            print()
            print(f"❌ Error: {type(ae).__name__}: {ae}")
            print("Press Enter to exit...")
            input()
            
else:
    
    try:
        
        import torch
        
        print(f"Torch already Installed")
        print(torch.__version__)
        
    except ImportError:
    
        print("Torch not installed")
        print()
        
        print("Installing Torch for CPU")
        print()
    
        try:
        
            check = subprocess.run(
                    
                    [sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio"],
                    capture_output = True,
                    text = True,
                    timeout = 1200

                )
                
            if check.returncode == 0:
                    
                print("Torch for CPU Installed Successfully")
                
                import torch
                
                print(torch.__version__)
                print()
            
            else:
                
                error = check.stdout[:300] if check.stdout else "unknown error"
                
                print(f"Torch for CPU could not be installed. Error: {error}...")
                print()
            
        except Exception as ae:
        
            print()
            print(f"❌ Error: {type(ae).__name__}: {ae}")
            print("Press Enter to exit...")
            input()
            
        
# Saves information in .txt
                        
with open("cache/computer_information.txt", "w") as data:
                        
    data.write(f"PYTHON_VERSION: 3.{sys.version_info.minor}\n")
    data.write(f"GPU: {gpu}\n")
    
print("Installation Complete Successfully")
print("Press Enter to exit...")
input()
