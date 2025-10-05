
import os
import json
import subprocess
import shlex

from utils.database import get_ffmpeg_folder_from_db

def ffmpeg_escape_text(text: str) -> str:
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace(':', '\\:')
    text = text.replace(',', '\\,')
    text = text.replace('\n', '\\n')
    return text

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
        # You can print or log line if needed
        # print(line)

    process.wait()

    return True if process.returncode == 0 else False

def run(
    input_video: str,
    caption_json: str,
    output_video: str,
    font_path: str = "assets/fonts/OpenSans-Regular.ttf",
    font_size: int = 48,
    font_color: str = "white",
    border_color: str = "black",
    border_size: int = 2,
    position: str = "bottom"  # or "top", or custom "x=...,y=..."
):
    """
    Burn captions into a video using drawtext and JSON segment timing.
    """
    with open(caption_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Build drawtext filters for each segment
    drawtext_filters = []
    for seg in data["segments"]:
        start = seg["start"]
        end = seg["end"]
        text = ffmpeg_escape_text(seg["text"])

        # Positioning
        if position == "bottom":
            pos_expr = "x=(w-text_w)/2:y=h-(text_h*2)"
        elif position == "top":
            pos_expr = "x=(w-text_w)/2:y=text_h"
        else:
            pos_expr = position  # custom, assuming it's already in "x=...:y=..." format

        drawtext = (
            f"drawtext=fontfile='{font_path}':"
            f"text='{text}':"
            f"enable='between(t,{start},{end})':"
            f"{pos_expr}:" # Directly embed the x=...:y=... expression here
            f"fontsize={font_size}:"
            f"fontcolor={font_color}:"
            f"borderw={border_size}:"
            f"bordercolor={border_color}"
        )
        drawtext_filters.append(drawtext)

    # Combine multiple drawtext filters using a comma (chained filters)
    vf_filter = ",".join(drawtext_filters)

    args = [
        "-y",
        "-i", input_video,
        "-vf", vf_filter,
        "-c:a", "copy",
        output_video
    ]

    # print(args)

    run_ffmpeg(args)
