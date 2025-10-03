
import os
import subprocess
import json

from utils.database import get_ffmpeg_folder_from_db

def get_ffprobe_path():
    ffmpeg_folder = get_ffmpeg_folder_from_db()
    ffprobe_path = os.path.join(ffmpeg_folder, 'bin', 'ffprobe.exe')
    if not os.path.isfile(ffprobe_path):
        raise FileNotFoundError(f'ffprobe.exe not found at: {ffprobe_path}')
    return ffprobe_path

def run(input_file: str) -> float:
    ffprobe_path = get_ffprobe_path()
    cmd = [
        ffprobe_path,
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'json',
        input_file
    ]

    result = subprocess.run(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")

    data = json.loads(result.stdout)
    duration = float(data['format']['duration'])
    return duration
