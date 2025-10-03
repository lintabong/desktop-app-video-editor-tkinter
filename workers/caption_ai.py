
import os
from faster_whisper import WhisperModel
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

from utils.paths import BASE_DIR


def add_subtitles_to_videos(
        video_paths: list[str],
        model_path: str = 'tools/faster-whisper-small',
        font_path: str = 'fonts/OpenSans-Regular.ttf',
        font_size: int = 48,
        font_color: str = 'white',
        stroke_color: str = 'black',
        stroke_width: int = 2,
        export_folder: str = 'output'):

    model_path = os.path.join(BASE_DIR, model_path)
    font_path = os.path.join(BASE_DIR, font_path)

    model = WhisperModel(model_path)

    os.makedirs(export_folder, exist_ok=True)

    for video_path in video_paths:
        filename = os.path.basename(video_path)
        name, ext = os.path.splitext(filename)
        export_path = os.path.join(export_folder, f'{name}_subtitled.mp4')

        print(f'🎬 Processing: {video_path}')
        print(f'📄 Export: {export_path}')

        # 1️⃣ Transcribe audio
        segments, info = model.transcribe(video_path, beam_size=5)
        print(f'Detected language: {info.language}')

        # 2️⃣ Load video
        video = VideoFileClip(video_path)

        # 3️⃣ Generate subtitle clips
        text_clips = []
        for seg in segments:
            text = seg.text.strip()
            if not text:
                continue

            start = seg.start
            end = seg.end
            duration = end - start

            # Calculate subtitle box width
            max_width = int(video.w * 0.8)
            y_position = video.h - int(video.h * 0.45)

            txt_clip = (
                TextClip(
                    text=text,
                    font=font_path,
                    font_size=font_size,
                    color=font_color,
                    stroke_color=stroke_color,
                    stroke_width=stroke_width,
                    method='caption',
                    size=(max_width, None),
                    text_align='center'
                )
                .with_position(('center', y_position))
                .with_start(start)
                .with_duration(duration)
            )

            text_clips.append(txt_clip)

        # 4️⃣ Combine original video + subtitles
        final = CompositeVideoClip([video] + text_clips)

        # 5️⃣ Export
        final.write_videofile(
            export_path,
            codec='libx264',    # good for mp4
            audio_codec='aac',  # keep audio
            fps=video.fps
        )

        print(f'✅ Finished: {export_path}')
