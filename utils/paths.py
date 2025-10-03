
import os
import sys

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath('.')

BASE_DIR = get_base_dir()
CONFIG_PATH = os.path.join('config', 'settings.json')

BASE_DATABASE_PATH = 'database'
