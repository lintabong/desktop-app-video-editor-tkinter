pip install pyinstaller
pyinstaller --onefile stt_worker.py
# result: dist/stt_worker.exe (on Windows) or dist/stt_worker (on Linux/Mac)


distribute
dist/stt_worker.exe
model/   <-- keep this folder next to exe

### example run
python stt_worker.py --input C:\Users\Dell^ 5320\Documents\desktop-app-video-editor-tkinter\examples\test_0.mp4 --model tools/faster-whisper-small --lang id --beam 5 --output result.json

### 1 clean up old builds
rmdir /s /q build
rmdir /s /q dist
del stt_worker.spec

### 2 make exe file
pyinstaller --onefile stt_worker.py
pyinstaller --onefile --noconsole stt_worker.py

