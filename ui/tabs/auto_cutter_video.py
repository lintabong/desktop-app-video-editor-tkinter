
import os
import re
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

from workers import get_video_duration, video_trimmer_manual


class AutoCutterVideoTab:
    def __init__(self, parent):
        self.frame = parent
        self.master_video_path = None
        self.output_folder = 'output'
        self.worker = None

        self.init_ui()

    def _create_button(self, frame, text, command):
        btn_master_video = ctk.CTkButton(
            frame,
            text=text,
            height=50,
            font=ctk.CTkFont(size=14),
            command=command,
            fg_color='#e74c3c' if re.search(r'✂️', text) else None,
            hover_color='#c0392b' if re.search(r'✂️', text) else None,
        )
        btn_master_video.pack(side="left", fill="x", expand=True, padx=(0, 10))

    def init_ui(self):
        main_container = ctk.CTkFrame(self.frame, fg_color='transparent')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        top_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        top_frame.pack(fill='x', pady=(0, 20))

        self._create_button(top_frame, '📹 Pilih Master Video', self.select_master_video)
        self._create_button(top_frame, '📁 Pilih Output Folder', self.select_output_folder)
        self._create_button(top_frame, '✂️ Jalankan Auto Cutter', self.start_auto_cutter)

        # === Configuration Section ===
        config_section = ctk.CTkFrame(main_container, fg_color="transparent")
        config_section.pack(fill='x', pady=(0, 20))

        # Mode
        mode_frame = ctk.CTkFrame(config_section, fg_color="transparent")
        mode_frame.pack(fill='x', pady=(0, 15))

        mode_label = ctk.CTkLabel(
            mode_frame,
            text='Mode',
            width=150,
            anchor='w',
            font=ctk.CTkFont(size=13)
        )
        mode_label.pack(side='left', padx=(0, 20))

        self.mode_combo = ctk.CTkComboBox(
            mode_frame,
            values=['Manual Interval', 'AI Scene Detect (Scenedetect)'],
            width=1400,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.mode_combo.set('Manual Interval')
        self.mode_combo.pack(side='left', fill='x', expand=True)

        # Interval (detik)
        interval_frame = ctk.CTkFrame(config_section, fg_color="transparent")
        interval_frame.pack(fill="x", pady=(0, 15))

        interval_label = ctk.CTkLabel(
            interval_frame,
            text='Interval (detik)',
            width=150,
            anchor='w',
            font=ctk.CTkFont(size=13)
        )
        interval_label.pack(side='left', padx=(0, 20))

        self.interval_entry = ctk.CTkEntry(
            interval_frame,
            width=400,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.interval_entry.insert(0, "6.00")
        self.interval_entry.pack(side="left", fill="x", expand=True)

        # Sensitivity (AI)
        sensitivity_frame = ctk.CTkFrame(config_section, fg_color="transparent")
        sensitivity_frame.pack(fill="x")

        sensitivity_label = ctk.CTkLabel(
            sensitivity_frame,
            text='Sensitivity (AI)',
            width=150,
            anchor='w',
            font=ctk.CTkFont(size=13)
        )
        sensitivity_label.pack(side="left", padx=(0, 20))

        self.sensitivity_entry = ctk.CTkEntry(
            sensitivity_frame,
            width=400,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.sensitivity_entry.insert(0, '12.00')
        self.sensitivity_entry.pack(side='left', fill='x', expand=True)

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
        self.status_textbox.insert('1.0', 'Ready to process video...\n')
        self.status_textbox.configure(state='disabled')

    def select_master_video(self):
        file_path = filedialog.askopenfilename(
            title='Pilih Master Video',
            filetypes=[
                ('Video files', '*.mp4 *.avi *.mov *.mkv *.flv *.wmv'),
                ('All files', '*.*')
            ]
        )
        if file_path:
            self.master_video_path = file_path

    def select_output_folder(self):
        folder_path = filedialog.askdirectory(title='Pilih Output Folder')
        if folder_path:
            self.output_folder = folder_path

    def start_auto_cutter(self):
        if not self.master_video_path:
            messagebox.showwarning('Warning', 'Please select a master video first!')
            return

        thread = threading.Thread(target=self._run_auto_cutter_task, daemon=True)
        thread.start()

    def _run_auto_cutter_task(self):
        self.clear_status()

        mode = self.mode_combo.get()
        interval = self.interval_entry.get()
        sensitivity = self.sensitivity_entry.get()

        duration = get_video_duration.run(self.master_video_path)

        start = 0
        part = 1
        total_output = int(-(-duration/float(interval) // 1))

        # Use .after() to update UI safely from thread
        self.log_status(f'\n▶ Starting Auto Trimmer...')
        self.log_status(f'Mode     : {mode}')
        self.log_status(f'Duration : {duration} Second')

        # self.frame.after(0, self.log_status,f'\n▶ Starting Auto Trimmer...' )

        while start < duration:
            current_duration = min(float(interval), duration - start)
            output_file = os.path.join(self.output_folder, f'part_{part:03d}.mp4')

            video_trimmer_manual.run(
                start,
                current_duration,
                self.master_video_path,
                output_file
            )

            self.log_status(f'Trim   : Part-{part}')

            start += current_duration
            part += 1

        self.log_status(f'✅ Finish')

    def log_status(self, message):
        self.status_textbox.configure(state='normal')
        self.status_textbox.insert('end', f'{message}\n')
        self.status_textbox.see('end')
        self.status_textbox.configure(state='disabled')

    def clear_status(self):
        self.status_textbox.configure(state='normal')
        self.status_textbox.delete('1.0', 'end')
        self.status_textbox.configure(state='disabled')
