
import asyncio
import edge_tts
import os

def run(text, voice, output_path) -> bool:
    """
    Generate TTS audio using Microsoft Edge voices.
    This function is blocking (sync) so it can be used inside threading.Thread.

    :param text: The text to convert to speech.
    :param voice: Voice short name (e.g. 'id-ID-ArdiNeural').
    :param output_path: Where to save the audio file (e.g. 'output.mp3').
    :return: True if successful, False otherwise.
    """
    async def _run_tts():
        tts = edge_tts.Communicate(text, voice=voice)
        await tts.save(output_path)

    try:
        asyncio.run(_run_tts())
        return True
    except Exception as e:
        print(f'TTS generation failed: {e}')
        return False
