
import os
import subprocess

from utils.database import get_transcriber_model_path, get_transcriber_wrapper_path

def run(input_file, output_file, beam):
    model_path = get_transcriber_model_path()
    exe_path = os.path.join(get_transcriber_wrapper_path(), 'stt_worker.exe')

    cmd = [
        exe_path,
        '--input', input_file,
        '--model', model_path,
        '--lang', 'id',
        '--beam', str(beam),
        '--output', output_file
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    process.wait()
    return True if process.returncode == 0 else False
