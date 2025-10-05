

import os
import subprocess

def run(input_file, output_file, beam):
    model_path = "assets/faster-whisper-small"

    exe_path = os.path.join('assets', 'stt_worker.exe')

    cmd = [
        exe_path,
        "--input", input_file,
        "--model", model_path,
        "--lang", "id",
        "--beam", str(beam),
        "--output", output_file
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    process.wait()
    return True if process.returncode == 0 else False

# run(
#     r"C:\Users\Dell 5320\Documents\desktop-app-video-editor-tkinter\examples\sound.mp3", 
#     'output/aa2.json',
#     5
# )
