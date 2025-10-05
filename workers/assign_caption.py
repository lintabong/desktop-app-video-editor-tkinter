import os
import json
import subprocess
import re

from utils.database import get_ffmpeg_folder_from_db


def ffmpeg_escape_text(text):
    text = text.replace('\\', '\\\\')
    text = text.replace("'", "'\\\\\\''")
    text = text.replace(':', '\\:')
    text = text.replace('%', '\\%')
    return text


def wrap_text(text, max_chars_per_line = 40):
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_length = len(word)
        # +1 for the space
        if current_length + word_length + len(current_line) > max_chars_per_line:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
            else:
                # Single word longer than max_chars_per_line
                lines.append(word)
                current_length = 0
        else:
            current_line.append(word)
            current_length += word_length
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)


def calculate_position(
    position: str,
    x_percent: float = None,
    y_percent: float = None
) -> str:
    """
    Calculate FFmpeg position expression based on position preset or percentages.
    
    Args:
        position (str): Position preset ('top', 'center', 'bottom', or 'custom')
        x_percent (float): X position as percentage (0-100)
        y_percent (float): Y position as percentage (0-100)
        
    Returns:
        str: FFmpeg position expression
    """
    if position == "bottom":
        return "x=(w-text_w)/2:y=h-th-20"
    elif position == "top":
        return "x=(w-text_w)/2:y=20"
    elif position == "center":
        return "x=(w-text_w)/2:y=(h-text_h)/2"
    elif position == "custom" and x_percent is not None and y_percent is not None:
        # Convert percentage to actual position
        # text_w and text_h are the text dimensions
        x_expr = f"(w*{x_percent/100})-(text_w/2)"
        y_expr = f"(h*{y_percent/100})-(text_h/2)"
        return f"x={x_expr}:y={y_expr}"
    else:
        # Assume position is already a valid expression like "x=100:y=200"
        return position


def build_drawtext_filter(
    segment: dict,
    font_path: str,
    font_size: int,
    font_color: str,
    border_color: str,
    border_size: int,
    position_expr: str,
    max_chars_per_line: int = 40,
    box_enabled: bool = False,
    box_color: str = "black@0.5",
    box_padding: int = 10
) -> str:
    start = segment["start"]
    end = segment["end"]
    
    # Wrap and escape text
    wrapped_text = wrap_text(segment["text"], max_chars_per_line)
    escaped_text = ffmpeg_escape_text(wrapped_text)
    
    # Build drawtext filter
    drawtext_parts = [
        f"drawtext=fontfile='{font_path}'",
        f"text='{escaped_text}'",
        f"fontsize={font_size}",
        f"fontcolor={font_color}",
        f"borderw={border_size}",
        f"bordercolor={border_color}",
        position_expr,
        f"enable='between(t,{start},{end})'",
    ]
    
    # Add text alignment for multi-line text
    drawtext_parts.append("line_spacing=5")
    
    # Optional: Add background box
    if box_enabled:
        drawtext_parts.extend([
            f"box=1",
            f"boxcolor={box_color}",
            f"boxborderw={box_padding}"
        ])
    
    return ":".join(drawtext_parts)


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
        # You can print or log line if needed for debugging
        # print(line)

    process.wait()

    return process.returncode == 0


def run(
    input_video: str,
    caption_json: str,
    output_video: str,
    font_path: str = 'assets/fonts/OpenSans-Regular.ttf',
    font_size: int = 48,
    font_color: str = 'white',
    border_color: str = 'black',
    border_size: int = 0,
    position: str = 'custom',  # "top", "center", "bottom", or "custom"
    x_percent: float = 50,  # X position as percentage (0-100) when position="custom"
    y_percent: float = 80,  # Y position as percentage (0-100) when position="custom"
    max_chars_per_line: int = 40,  # Maximum characters per line before wrapping
    box_enabled: bool = False,  # Enable background box behind text
    box_color: str = 'black@0.5',  # Box color with alpha (0.0-1.0)
    box_padding: int = 10  # Padding around text in box
):
    # Load caption data
    with open(caption_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Calculate position expression
    position_expr = calculate_position(position, x_percent, y_percent)

    # Build drawtext filters for each segment
    drawtext_filters = []
    for segment in data['segments']:
        drawtext_filter = build_drawtext_filter(
            segment=segment,
            font_path=font_path,
            font_size=font_size,
            font_color=font_color,
            border_color=border_color,
            border_size=border_size,
            position_expr=position_expr,
            max_chars_per_line=max_chars_per_line,
            box_enabled=box_enabled,
            box_color=box_color,
            box_padding=box_padding
        )
        drawtext_filters.append(drawtext_filter)

    # Combine multiple drawtext filters
    vf_filter = ",".join(drawtext_filters)

    # Build FFmpeg arguments
    args = [
        '-y',  # Overwrite output file
        '-i', input_video,
        '-vf', vf_filter,
        '-c:a', 'copy',  # Copy audio without re-encoding
        '-c:v', 'libx264',  # Video codec
        '-preset', 'medium',  # Encoding preset
        '-crf', '23',  # Quality (lower = better, 18-28 is reasonable)
        output_video
    ]

    return run_ffmpeg(args)
