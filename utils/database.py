import os
import sqlite3

from utils.paths import BASE_DATABASE_PATH

DATABASE_PATH = os.path.join(BASE_DATABASE_PATH, 'job_trimmer.db')

def init_config_db():
    DATABASE_PATH = os.path.join(BASE_DATABASE_PATH, 'settings.db')
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    # Insert default values if not present
    defaults = {
        'transcriber_model_path_folder': 'assets/faster-whisper-small',
        'ffmpeg_path_folder': 'assets/ffmpeg',
        'font_path_folder': 'assets/fonts',
    }

    for key, value in defaults.items():
        c.execute("""
            INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)
        """, (key, value))

    conn.commit()
    conn.close()

def get_ffmpeg_folder_from_db(db_path='database/settings.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = ?", ("ffmpeg_path_folder",))
    row = c.fetchone()
    conn.close()

    if row:
        ffmpeg_folder = os.path.abspath(row[0])
        return ffmpeg_folder
    else:
        raise KeyError('ffmpeg_path_folder not found in settings table')
