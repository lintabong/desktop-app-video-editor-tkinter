
import os
import subprocess

from utils.database import get_ffmpeg_folder_from_db


def run_ffmpeg(args: list[str]):
    ffmpeg_path = os.path.join(get_ffmpeg_folder_from_db(), 'bin', 'ffmpeg.exe')
    if not os.path.isfile(ffmpeg_path):
        raise FileNotFoundError(f'ffmpeg.exe not found at: {ffmpeg_path}')

    cmd = [ffmpeg_path] + args

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        universal_newlines=True,
        bufsize=1
    )

    for line in process.stderr:
        line = line.strip()

    process.wait()

    if process.returncode != 0:
        raise RuntimeError(f'❌ FFmpeg failed with code {process.returncode}')
    else:
        print('✅ FFmpeg completed successfully!')

def run(start, current_duration, input_path, output_path):
    args = [
        "-y",
        "-ss", str(start),
        "-t", str(current_duration),
        "-i", input_path,
        "-c", 'copy',
        output_path
    ]

    run_ffmpeg(args)
