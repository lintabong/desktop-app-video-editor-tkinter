
import os
import json
import argparse
from faster_whisper import WhisperModel

def transcribe_audio(input_path: str, model_path: str, language: str, beam_size: int, output_path: str):
    if not os.path.isfile(input_path):
        print(f"Input file not found: {input_path}")
        return

    print(f"Loading model from: {model_path}")
    model = WhisperModel(model_path, device="cpu", compute_type="int8")

    print(f"Transcribing: {input_path}")
    segments, info = model.transcribe(
        input_path,
        beam_size=beam_size,
        language=language
    )

    results = []
    for segment in segments:
        results.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Save transcription to JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "language": info.language,
            "duration": info.duration,
            "segments": results
        }, f, ensure_ascii=False, indent=2)

    print(f"Transcription saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STT Worker using faster-whisper")
    parser.add_argument("--input", required=True, help="Path to input audio file")
    parser.add_argument("--model", required=True, help="Path to model folder")
    parser.add_argument("--lang", required=True, help="Language code (e.g. 'id')")
    parser.add_argument("--beam", type=int, default=5, help="Beam size for decoding")
    parser.add_argument("--output", required=True, help="Path to save output JSON file")

    args = parser.parse_args()

    transcribe_audio(
        input_path=args.input,
        model_path=args.model,
        language=args.lang,
        beam_size=args.beam,
        output_path=args.output
    )
