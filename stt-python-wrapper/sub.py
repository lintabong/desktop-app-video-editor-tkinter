import subprocess

subprocess.run([
    'python', "stt_worker.py",
    '--input', r"C:\Users\Dell 5320\Documents\desktop-app-video-editor-tkinter\examples\sound.mp3",
    "--model", "faster-whisper-small",
    "--lang", "id",
    "--beam", "5",
    "--output", "res/result.json"
])