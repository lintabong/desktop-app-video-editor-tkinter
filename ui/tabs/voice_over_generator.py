
import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

from workers import generate_voice_over


class VoiceOverGeneratorTab:
    def __init__(self, parent):
        self.frame = parent
        # self.video_source_path = None
        self.output_file = 'output.mp3'
        self.voice = None
        self.text = None
        self.worker = None

        self.init_ui()

    def init_ui(self):
        main_container = ctk.CTkFrame(self.frame, fg_color='transparent')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # === Output Folder Section ===
        output_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        output_frame.pack(fill='x', pady=(0, 15))

        output_label = ctk.CTkLabel(
            output_frame,
            text='Output File:',
            width=120,
            anchor='w',
            font=ctk.CTkFont(size=13)
        )
        output_label.pack(side='left', padx=(0, 10))

        self.output_entry = ctk.CTkEntry(
            output_frame,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        self.output_entry.insert(0, self.output_file)
        self.output_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))

        output_browse_btn = ctk.CTkButton(
            output_frame,
            text='...',
            width=50,
            height=35,
            font=ctk.CTkFont(size=13),
            command=self.select_output_file
        )
        output_browse_btn.pack(side='left')

        # === Script VO Section ===
        script_label = ctk.CTkLabel(
            main_container,
            text='Script Voice Over:',
            font=ctk.CTkFont(size=13),
            anchor='w'
        )
        script_label.pack(anchor='w', pady=(0, 10))

        self.script_textbox = ctk.CTkTextbox(
            main_container,
            height=150,
            font=ctk.CTkFont(size=12)
        )
        self.script_textbox.pack(fill='x', pady=(0, 15))
        self.script_textbox.insert('1.0', '')

        # === Voice Section ===
        voice_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        voice_frame.pack(fill='x', pady=(0, 15))

        voice_label = ctk.CTkLabel(
            voice_frame,
            text='Voice:',
            width=120,
            anchor='w',
            font=ctk.CTkFont(size=13)
        )
        voice_label.pack(side='left', padx=(0, 10))

        self.voice_combo = ctk.CTkComboBox(
            voice_frame,
            values=['id-ID-GadisNeural', 'id-ID-ArdiNeural'],
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.voice_combo.set('id-ID-GadisNeural')
        self.voice_combo.pack(side='left', fill='x', expand=True)

        # === Run Button ===
        run_btn = ctk.CTkButton(
            main_container,
            text='🚀 Generate Voice Over',
            height=50,
            font=ctk.CTkFont(size=14, weight='bold'),
            fg_color='#7c3aed',
            hover_color='#6d28d9',
            command=self.run_clipbot
        )
        run_btn.pack(fill='x', pady=(0, 20))

        # === Status Section ===
        status_section = ctk.CTkFrame(main_container, fg_color='transparent')
        status_section.pack(fill='both', expand=True)

        status_label = ctk.CTkLabel(
            status_section,
            text='Status',
            font=ctk.CTkFont(size=14, weight='bold'),
            text_color='#8a8a9a'
        )
        status_label.pack(anchor='w', pady=(0, 10))

        self.status_textbox = ctk.CTkTextbox(
            status_section,
            height=200,
            font=ctk.CTkFont(size=12)
        )
        self.status_textbox.pack(fill='both', expand=True)
        self.status_textbox.insert('1.0', 'Ready to process clips...\n')
        self.status_textbox.configure(state='disabled')

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(
            title='Select Output File',
            defaultextension='.mp3',
            filetypes=[('MP3 files', '*.mp3'), ('All files', '*.*')]
        )
        if file_path:
            self.output_file = file_path
            self.output_entry.delete(0, 'end')
            self.output_entry.insert(0, file_path)

    def run_clipbot(self):
        script = self.script_textbox.get('1.0', 'end').strip()
        if not script or script == 'Tempel teks VO di sini.\nBaris kosong = pemisah.\n1 baris = 1 video.':
            messagebox.showwarning('Warning', 'Please enter a script!')
            return

        thread = threading.Thread(target=self._run_clipbot_task, daemon=True)
        thread.start()

    def _run_clipbot_task(self):
        self.log_status('Memulai proses generator voice over')
        task = generate_voice_over.run(
            text=self.script_textbox.get('1.0', 'end').strip(),
            voice=self.voice_combo.get(),
            output_path=self.output_file
        )

        self.log_status(f'Menggunakan suara {self.voice_combo.get()}')
        self.log_status(f'Output file -> {self.output_file}')
        if task:
            self.log_status(f'Sukses')
        else:
            self.log_status(f'Gagal')


    def log_status(self, message):
        self.status_textbox.configure(state='normal')
        self.status_textbox.insert('end', f'{message}\n')
        self.status_textbox.see('end')
        self.status_textbox.configure(state='disabled')
