
import os
import re
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
from tkinter import ttk

from workers import generate_caption, assign_caption
from utils.database import get_font_folder_from_db


class CaptionAiTab:
    def __init__(self, parent):
        self.frame = parent
        self.video_files = []
        self.output_folder = ''
        self.init_ui()

    def _create_button(self, frame, text, command):
        btn_master_video = ctk.CTkButton(
            frame,
            text=text,
            height=50,
            font=ctk.CTkFont(size=14),
            command=command,
            fg_color='#7c3aed' if re.search(r'🚀', text) else None,
            hover_color='#6d28d9' if re.search(r'🚀', text) else None,
        )
        btn_master_video.pack(side="left", fill="x", expand=True, padx=(0, 10))

    def init_ui(self):
        main_container = ctk.CTkFrame(self.frame, fg_color='transparent')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # === Top Buttons Section ===
        top_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        top_frame.pack(fill='x', pady=(0, 15))

        self._create_button(top_frame, '📹 Tambah Video', self.add_video)
        self._create_button(top_frame, '📁 Tambah Folder', self.add_folder)
        self._create_button(top_frame, '📂 Output Folder', self.select_output_folder)
        self._create_button(top_frame, '🚀 Mulai Batch Caption', self.start_batch_caption)

        # === Table Section ===
        table_frame = ctk.CTkFrame(main_container, fg_color='#1e1e2e', corner_radius=10)
        table_frame.pack(fill='both', expand=True, pady=(0, 15))

        # Create Treeview with scrollbar
        tree_container = ctk.CTkFrame(table_frame, fg_color='transparent')
        tree_container.pack(fill='both', expand=True, padx=0, pady=0)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_container)
        scrollbar.pack(side='right', fill='y')

        style = ttk.Style(self.frame)
        style.theme_use('clam') 

        custom_style_name = "Modern.Treeview"

        style.configure(
            custom_style_name,
            background="#2B2B2B",      # table background
            foreground="#FFFFFF",      # text color
            fieldbackground="#2B2B2B",
            rowheight=28,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        # 🧭 Header styling
        style.configure(
            "Modern.Treeview.Heading",
            background="#3A3A3A",
            foreground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            padding=(8, 5),
            borderwidth=0
        )
        style.map("Modern.Treeview.Heading",
                background=[("active", "#4A4A4A")])

        # Treeview
        self.tree = ttk.Treeview(
            tree_container,
            columns=('namefile', 'progress', 'action'),
            show='headings',
            height=5,
            style=custom_style_name,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        # Define headings
        self.tree.heading('namefile', text='Nama File')
        self.tree.heading('progress', text='Progress')
        self.tree.heading('action', text='Action')

        # Define columns
        self.tree.column('namefile', width=400, anchor='w')
        self.tree.column('progress', width=150, anchor='center')
        self.tree.column('action', width=100, anchor='center')

        self.tree.pack(fill='both', expand=True)

        # Bind double-click to delete
        self.tree.bind('<Double-Button-1>', self.delete_selected)

        # === Caption Style Section ===
        style_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        style_frame.pack(fill='x', pady=(0, 15))

        # style_label = ctk.CTkLabel(
        #     style_frame,
        #     text='Caption Style',
        #     font=ctk.CTkFont(size=14, weight='bold'),
        #     text_color='#8a8a9a'
        # )
        # style_label.pack(anchor='w', pady=(0, 10))

        # Grid container for style options (3 columns x 2 rows)
        grid_container = ctk.CTkFrame(style_frame, fg_color='transparent')
        grid_container.pack(fill='x')

        # Row 1
        # Style Pack
        style_pack_frame = ctk.CTkFrame(grid_container, fg_color='transparent')
        style_pack_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky='ew')

        style_pack_label = ctk.CTkLabel(
            style_pack_frame,
            text='Style Pack:',
            font=ctk.CTkFont(size=12),
            anchor='w'
        )
        style_pack_label.pack(anchor='w', pady=(0, 5))

        self.style_pack_combo = ctk.CTkComboBox(
            style_pack_frame,
            values=['Classic', 'Modern', 'Minimal'],
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.style_pack_combo.set('Classic')
        self.style_pack_combo.pack(fill='x')

        # Mode
        mode_frame = ctk.CTkFrame(grid_container, fg_color='transparent')
        mode_frame.grid(row=0, column=1, padx=(0, 10), pady=(0, 10), sticky='ew')

        mode_label = ctk.CTkLabel(
            mode_frame,
            text='Mode:',
            font=ctk.CTkFont(size=12),
            anchor='w'
        )
        mode_label.pack(anchor='w', pady=(0, 5))

        self.mode_combo = ctk.CTkComboBox(
            mode_frame,
            values=['Word', 'Full', 'Line'],
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.mode_combo.set('Word')
        self.mode_combo.pack(fill='x')

        # Text Color
        text_color_frame = ctk.CTkFrame(grid_container, fg_color='transparent')
        text_color_frame.grid(row=0, column=2, pady=(0, 10), sticky='ew')

        text_color_label = ctk.CTkLabel(
            text_color_frame,
            text='Text Color:',
            font=ctk.CTkFont(size=12),
            anchor='w'
        )
        text_color_label.pack(anchor='w', pady=(0, 5))

        self.text_color_btn = ctk.CTkButton(
            text_color_frame,
            text='#FFFFFF',
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color='#FFFFFF',
            text_color='#000000',
            hover_color='#e0e0e0',
            command=self.pick_text_color
        )
        self.text_color_btn.pack(fill='x')
        self.selected_color = '#FFFFFF'

        # Row 2
        # Font
        font_frame = ctk.CTkFrame(grid_container, fg_color='transparent')
        font_frame.grid(row=1, column=0, padx=(0, 10), sticky='ew')

        font_label = ctk.CTkLabel(
            font_frame,
            text='Font:',
            font=ctk.CTkFont(size=12),
            anchor='w'
        )
        font_label.pack(anchor='w', pady=(0, 5))

        self.font_combo = ctk.CTkComboBox(
            font_frame,
            values=self.get_available_fonts(),
            height=35,
            font=ctk.CTkFont(size=12)
        )
        if self.font_combo.cget('values'):
            self.font_combo.set(self.font_combo.cget('values')[0])
        self.font_combo.pack(fill='x')

        # Font Size
        font_size_frame = ctk.CTkFrame(grid_container, fg_color='transparent')
        font_size_frame.grid(row=1, column=1, padx=(0, 10), sticky='ew')

        font_size_label = ctk.CTkLabel(
            font_size_frame,
            text='Font Size:',
            font=ctk.CTkFont(size=12),
            anchor='w'
        )
        font_size_label.pack(anchor='w', pady=(0, 5))

        self.font_size_entry = ctk.CTkEntry(
            font_size_frame,
            height=35,
            font=ctk.CTkFont(size=12),
            placeholder_text='48'
        )
        self.font_size_entry.insert(0, '48')
        self.font_size_entry.pack(fill='x')

        # Configure grid weights
        grid_container.grid_columnconfigure(0, weight=1)
        grid_container.grid_columnconfigure(1, weight=1)
        grid_container.grid_columnconfigure(2, weight=1)

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
            height=150,
            font=ctk.CTkFont(size=12)
        )
        self.status_textbox.pack(fill='both', expand=True)
        self.status_textbox.insert('1.0', 'Ready to add videos and start batch captioning...\n')
        self.status_textbox.configure(state='disabled')

    def get_available_fonts(self):
        fonts_dir = 'assets/fonts'
        if os.path.exists(fonts_dir):
            fonts = [f for f in os.listdir(fonts_dir) if f.endswith(('.ttf', '.otf'))]
            return fonts if fonts else ['Default']
        return ['Default']

    def add_video(self):
        file_paths = filedialog.askopenfilenames(
            title='Select Video Files',
            filetypes=[
                ('Video files', '*.mp4 *.avi *.mov *.mkv *.flv *.wmv'),
                ('All files', '*.*')
            ]
        )
        for file_path in file_paths:
            if file_path not in self.video_files:
                self.video_files.append(file_path)
                filename = os.path.basename(file_path)
                self.tree.insert('', 'end', values=(filename, 'Pending', 'Delete'))
                self.log_status(f'Added: {filename}')

    def add_folder(self):
        folder_path = filedialog.askdirectory(title='Select Folder with Videos')
        if folder_path:
            video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(video_extensions):
                    file_path = os.path.join(folder_path, filename)
                    if file_path not in self.video_files:
                        self.video_files.append(file_path)
                        self.tree.insert('', 'end', values=(filename, 'Pending', 'Delete'))
            self.log_status(f'Added videos from folder: {folder_path}')

    def select_output_folder(self):
        folder_path = filedialog.askdirectory(title='Select Output Folder')
        if folder_path:
            self.output_folder = folder_path
            self.log_status(f'Output folder set: {folder_path}')

    def delete_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            filename = item['values'][0]
            
            # Find and remove from video_files list
            for i, video_path in enumerate(self.video_files):
                if os.path.basename(video_path) == filename:
                    del self.video_files[i]
                    break
            
            self.tree.delete(selected_item[0])
            self.log_status(f'Removed: {filename}')

    def pick_text_color(self):
        color = colorchooser.askcolor(title='Pick Text Color', initialcolor=self.selected_color)
        if color[1]:
            self.selected_color = color[1]
            self.text_color_btn.configure(text=self.selected_color, fg_color=self.selected_color)
            # Adjust text color for visibility
            rgb = tuple(int(self.selected_color[i:i+2], 16) for i in (1, 3, 5))
            brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
            text_color = '#000000' if brightness > 128 else '#FFFFFF'
            self.text_color_btn.configure(text_color=text_color)

    def start_batch_caption(self):
        if not self.video_files:
            messagebox.showwarning('Warning', 'Please add at least one video file!')
            return

        if not self.output_folder:
            messagebox.showwarning('Warning', 'Please select an output folder!')
            return

        try:
            font_size = int(self.font_size_entry.get())
            if font_size <= 0:
                messagebox.showwarning('Warning', 'Font size must be positive!')
                return
        except ValueError:
            messagebox.showwarning('Warning', 'Please enter a valid font size!')
            return

        thread = threading.Thread(target=self._run_batch_caption, daemon=True)
        thread.start()

    def _run_batch_caption(self):
        for idx, video_path in enumerate(self.video_files):
            filename = os.path.basename(video_path)
            self.log_status(f'Processing ({idx+1}/{len(self.video_files)}): {filename}')

            # Update tree progress
            self.update_row_table(filename, 'Generate Caption')

            video_format = filename.split('.')[1]

            output_filename = re.sub(r'.mp4|.avi|.mov|.mkv|.flv|.wmv', '.json', filename)
            output_filename_srt = re.sub(r'.json', '.srt', output_filename)
            output_path = os.path.join(self.output_folder, output_filename)

            result_generate_caption = generate_caption.run(
                video_path, 
                output_path, 
                5
            )

            output_video_path = os.path.join(self.output_folder, filename.split('.')[0] +'_caption.'+ video_format)

            if not result_generate_caption:
                self.update_row_table(filename, 'Error ❌ Generate Caption')

            self.update_row_table(filename, 'Apply Caption to video')

            # json_to_srt(output_path, os.path.join(self.output_folder, output_filename_srt))
            font_folder_path = get_font_folder_from_db()
            print(self.font_combo.get())
            font_path = os.path.join(font_folder_path, self.font_combo.get())
            print(font_path)
            print(font_folder_path)
            result_apply_caption = assign_caption.run(
                input_video=video_path,
                caption_json=output_path,
                output_video=output_video_path,
                font_path='assets/fonts/OpenSans-Regular.ttf',
                font_size=int(self.font_size_entry.get()),
                font_color=self.selected_color
            )

            if not result_apply_caption:
                self.update_row_table(filename, 'Error ❌ Apply Caption')

            self.update_row_table(filename, 'Completed ✅')

            # self.log_status(f'✅ Completed: {filename}')

        # self.log_status('='*50)
        self.log_status('🎉 Batch caption process completed!')
        # self.log_status('='*50)

    def update_row_table(self, filename, message):
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == filename:
                self.tree.item(item, values=(filename, message, 'Delete'))
                break

    def log_status(self, message):
        self.status_textbox.configure(state='normal')
        self.status_textbox.insert('end', f'{message}\n')
        self.status_textbox.see('end')
        self.status_textbox.configure(state='disabled')
