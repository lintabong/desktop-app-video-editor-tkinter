
import os
import subprocess
from utils.database import get_ffmpeg_folder_from_db

def run_ffmpeg(args: list[str]) -> bool:
    ffmpeg_path = os.path.join(get_ffmpeg_folder_from_db(), 'bin', 'ffmpeg.exe')
    if not os.path.isfile(ffmpeg_path):
        raise FileNotFoundError(f'❌ ffmpeg.exe not found at: {ffmpeg_path}')

    cmd = [ffmpeg_path] + args

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        universal_newlines=True,
        bufsize=1
    )

    process.wait()

    if process.returncode != 0:
        print(f'❌ FFmpeg failed with code {process.returncode}')
        return False
    else:
        print('✅ FFmpeg completed successfully!')
        return True


def run(video_path, audio_path, start_time, output_path):
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return False

    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return False

    # Overwrite if exists
    if os.path.exists(output_path):
        os.remove(output_path)

    if start_time >= 0:
        delay_ms = int(start_time * 1000)
        args = [
            "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-af", f"adelay={delay_ms}|{delay_ms}",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest", 
            output_path
        ]
    else:
        args = [
            "-y",
            "-i", video_path,
            "-ss", str(abs(start_time)),
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            output_path
        ]

    return run_ffmpeg(args)
