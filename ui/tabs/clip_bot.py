
import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox


class ClipBotTab:
    def __init__(self, parent):
        self.frame = parent
        self.video_source_path = None
        self.output_folder = 'output'
        self.worker = None

        self.init_ui()

    def init_ui(self):
        main_container = ctk.CTkFrame(self.frame, fg_color='transparent')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # === Video Sumber Section ===
        video_source_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        video_source_frame.pack(fill='x', pady=(0, 15))

        video_label = ctk.CTkLabel(
            video_source_frame,
            text='Video Sumber:',
            width=120,
            anchor='w',
            font=ctk.CTkFont(size=13)
        )
        video_label.pack(side='left', padx=(0, 10))

        self.video_entry = ctk.CTkEntry(
            video_source_frame,
            placeholder_text='',
            height=35,
            font=ctk.CTkFont(size=13)
        )
        self.video_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))

        video_browse_btn = ctk.CTkButton(
            video_source_frame,
            text='...',
            width=50,
            height=35,
            font=ctk.CTkFont(size=13),
            command=self.select_video_source
        )
        video_browse_btn.pack(side='left')

        # === Output Folder Section ===
        output_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        output_frame.pack(fill='x', pady=(0, 15))

        output_label = ctk.CTkLabel(
            output_frame,
            text='Output Folder:',
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
        self.output_entry.insert(0, 'output')
        self.output_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))

        output_browse_btn = ctk.CTkButton(
            output_frame,
            text='...',
            width=50,
            height=35,
            font=ctk.CTkFont(size=13),
            command=self.select_output_folder
        )
        output_browse_btn.pack(side='left')

        # === Script VO Section ===
        script_label = ctk.CTkLabel(
            main_container,
            text='Script VO',
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
        self.script_textbox.insert('1.0', 'Tempel teks VO di sini.')

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
            text='🚀 Jalankan ClipBot',
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

    def select_video_source(self):
        file_path = filedialog.askopenfilename(
            title='Pilih Video Sumber',
            filetypes=[
                ('Video files', '*.mp4 *.avi *.mov *.mkv *.flv *.wmv'),
                ('All files', '*.*')
            ]
        )
        if file_path:
            self.video_source_path = file_path
            self.video_entry.delete(0, 'end')
            self.video_entry.insert(0, file_path)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory(title='Pilih Output Folder')
        if folder_path:
            self.output_folder = folder_path
            self.output_entry.delete(0, 'end')
            self.output_entry.insert(0, folder_path)

    def run_clipbot(self):
        if not self.video_source_path:
            messagebox.showwarning('Warning', 'Please select a video source first!')
            return

        script = self.script_textbox.get('1.0', 'end').strip()
        if not script or script == 'Tempel teks VO di sini.\nBaris kosong = pemisah.\n1 baris = 1 video.':
            messagebox.showwarning('Warning', 'Please enter a script!')
            return

        thread = threading.Thread(target=self._run_clipbot_task, daemon=True)
        thread.start()

    def _run_clipbot_task(self):
        self.log_status("Starting ClipBot processing...")
        # Implement your ClipBot logic here
        pass

    def log_status(self, message):
        self.status_textbox.configure(state='normal')
        self.status_textbox.insert('end', f'{message}\n')
        self.status_textbox.see('end')
        self.status_textbox.configure(state='disabled')
