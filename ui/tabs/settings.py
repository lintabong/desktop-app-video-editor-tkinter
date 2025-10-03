
import os
import json
import customtkinter as ctk

from utils.paths import CONFIG_PATH


class SettingsTab:
    def __init__(self, parent):
        self.frame = parent

        self.settings = self._load_settings()

        title = ctk.CTkLabel(
            self.frame,
            text='⚙️ Settings',
            font=ctk.CTkFont(size=18, weight='bold')
        )
        title.pack(pady=(10, 20))

        self._create_entry_row(label='Transriber Model Path', key='transcriber_model_path_folder')
        self._create_entry_row(label='FFMPEG Path', key='ffmpeg_path_folder')
        self._create_entry_row(label='Fonts Path', key='font_path_folder')

        save_btn = ctk.CTkButton(
            self.frame,
            text='💾 Save Settings',
            command=self.save_settings
        )
        save_btn.pack(pady=(20, 10))

        self.status_label = ctk.CTkLabel(
            self.frame,
            text='',
            text_color='#8a8a9a',
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack()

    def _create_entry_row(self, label: str, key: str):
        frame = ctk.CTkFrame(self.frame, fg_color='transparent')
        frame.pack(fill='x', pady=(5, 5), padx=20)

        lbl = ctk.CTkLabel(frame, text=label, width=150, anchor='w')
        lbl.pack(side='left', padx=(0, 10))

        entry = ctk.CTkEntry(frame)
        entry.insert(0, str(self.settings.get(key, '')))
        entry.pack(side='left', fill='x', expand=True)

        setattr(self, f'{key}_entry', entry)

    def _load_settings(self):
        if not os.path.exists(CONFIG_PATH):
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            self._save_json({
                'transcriber_model_path_folder': 'assets/faster-whisper-small',
                'ffmpeg_path_folder': 'assets/ffmpeg',
                'font_path_folder': 'assets/fonts',
            })
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_json(self, data):
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def save_settings(self):
        data = {
            'transcriber_model_path_folder': self.transcriber_model_path_folder_entry.get(),
            'ffmpeg_path_folder': self.ffmpeg_path_folder_entry.get(),
            'font_path_folder': self.font_path_folder_entry.get(),
        }
        self._save_json(data)
        self.status_label.configure(text='✅ Settings saved!')
