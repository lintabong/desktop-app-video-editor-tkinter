import subprocess

def run_stt_exe(input_file, output_file, beam):
    exe_path = "stt_worker.exe"
    model_path = "faster-whisper-small"

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
    print(True if process.returncode == 0 else False)

run_stt_exe(
    r"C:\Users\Dell 5320\Documents\desktop-app-video-editor-tkinter\examples\sound.mp3", 
    'res/aa2.json',
    5
)
