
import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

from workers import combine_audio_video


class AudioVideoCombinerTab:
    def __init__(self, parent):
        self.frame = parent
        self.video_path = None
        self.audio_path = None
        self.output_file = 'output_combined.mp4'
        self.worker = None

        self.init_ui()

    def init_ui(self):
        main_container = ctk.CTkFrame(self.frame, fg_color='transparent')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # === Video Input Section ===
        video_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        video_frame.pack(fill='x', pady=(0, 15))

        video_label = ctk.CTkLabel(
            video_frame,
            text='Video File:',
            width=120,
            anchor='w',
            font=ctk.CTkFont(size=13)
        )
        video_label.pack(side='left', padx=(0, 10))

        self.video_entry = ctk.CTkEntry(
            video_frame,
            height=35,
            font=ctk.CTkFont(size=13),
            placeholder_text='Select video file...'
        )
        self.video_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))

        video_browse_btn = ctk.CTkButton(
            video_frame,
            text='Browse',
            width=80,
            height=35,
            font=ctk.CTkFont(size=13),
            command=self.select_video_file
        )
        video_browse_btn.pack(side='left')

        # === Audio Input Section ===
        audio_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        audio_frame.pack(fill='x', pady=(0, 15))

        audio_label = ctk.CTkLabel(
            audio_frame,
            text='Audio File:',
            width=120,
            anchor='w',
            font=ctk.CTkFont(size=13)
        )
        audio_label.pack(side='left', padx=(0, 10))

        self.audio_entry = ctk.CTkEntry(
            audio_frame,
            height=35,
            font=ctk.CTkFont(size=13),
            placeholder_text='Select audio file...'
        )
        self.audio_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))

        audio_browse_btn = ctk.CTkButton(
            audio_frame,
            text='Browse',
            width=80,
            height=35,
            font=ctk.CTkFont(size=13),
            command=self.select_audio_file
        )
        audio_browse_btn.pack(side='left')

        # === Time Start Section ===
        time_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        time_frame.pack(fill='x', pady=(0, 15))

        time_label = ctk.CTkLabel(
            time_frame,
            text='Start Time (sec):',
            width=120,
            anchor='w',
            font=ctk.CTkFont(size=13)
        )
        time_label.pack(side='left', padx=(0, 10))

        self.time_entry = ctk.CTkEntry(
            time_frame,
            height=35,
            font=ctk.CTkFont(size=13),
            placeholder_text='0.0'
        )
        self.time_entry.insert(0, '0.0')
        self.time_entry.pack(side='left', fill='x', expand=True)

        time_info = ctk.CTkLabel(
            time_frame,
            text='(Time in seconds when audio starts)',
            font=ctk.CTkFont(size=11),
            text_color='#8a8a9a'
        )
        time_info.pack(side='left', padx=(10, 0))

        # === Output File Section ===
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

        # === Run Button ===
        run_btn = ctk.CTkButton(
            main_container,
            text='🎬 Combine Audio & Video',
            height=50,
            font=ctk.CTkFont(size=14, weight='bold'),
            fg_color='#7c3aed',
            hover_color='#6d28d9',
            command=self.run_combiner
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
        self.status_textbox.insert('1.0', 'Ready to combine audio and video...\n')
        self.status_textbox.configure(state='disabled')

    def select_video_file(self):
        file_path = filedialog.askopenfilename(
            title='Select Video File',
            filetypes=[
                ('Video files', '*.mp4 *.avi *.mov *.mkv *.flv *.wmv'),
                ('All files', '*.*')
            ]
        )
        if file_path:
            self.video_path = file_path
            self.video_entry.delete(0, 'end')
            self.video_entry.insert(0, file_path)

    def select_audio_file(self):
        file_path = filedialog.askopenfilename(
            title='Select Audio File',
            filetypes=[
                ('Audio files', '*.mp3 *.wav *.aac *.m4a *.ogg *.flac'),
                ('All files', '*.*')
            ]
        )
        if file_path:
            self.audio_path = file_path
            self.audio_entry.delete(0, 'end')
            self.audio_entry.insert(0, file_path)

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(
            title='Select Output File',
            defaultextension='.mp4',
            filetypes=[('MP4 files', '*.mp4'), ('All files', '*.*')]
        )
        if file_path:
            self.output_file = file_path
            self.output_entry.delete(0, 'end')
            self.output_entry.insert(0, file_path)

    def run_combiner(self):
        if not self.video_entry.get():
            messagebox.showwarning('Warning', 'Please select a video file!')
            return

        if not self.audio_entry.get():
            messagebox.showwarning('Warning', 'Please select an audio file!')
            return

        try:
            start_time = float(self.time_entry.get())
            if start_time < 0:
                messagebox.showwarning('Warning', 'Start time must be non-negative!')
                return
        except ValueError:
            messagebox.showwarning('Warning', 'Please enter a valid number for start time!')
            return

        thread = threading.Thread(target=self._run_combiner_task, daemon=True)
        thread.start()

    def _run_combiner_task(self):
        self.log_status('Memulai proses penggabungan audio dan video')
        self.log_status(f'Video: {self.video_entry.get()}')
        self.log_status(f'Audio: {self.audio_entry.get()}')
        self.log_status(f'Start time: {self.time_entry.get()} seconds')
        self.log_status(f'Output: {self.output_entry.get()}')
        
        try:
            task = combine_audio_video.run(
                video_path=self.video_entry.get(),
                audio_path=self.audio_entry.get(),
                start_time=float(self.time_entry.get()),
                output_path=self.output_entry.get()
            )

            if task:
                self.log_status('✅ Sukses! Video berhasil digabungkan dengan audio.')
            else:
                self.log_status('❌ Gagal menggabungkan audio dan video.')
        except Exception as e:
            self.log_status(f'❌ Error: {str(e)}')

    def log_status(self, message):
        self.status_textbox.configure(state='normal')
        self.status_textbox.insert('end', f'{message}\n')
        self.status_textbox.see('end')
        self.status_textbox.configure(state='disabled')
