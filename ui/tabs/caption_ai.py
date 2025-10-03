import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import colorchooser
from customtkinter.windows import CTkToplevel, CTkInputDialog

# from core.caption_worker import CaptionWorker
from utils.paths import BASE_DIR


class CaptionAiTab:
    def __init__(self, parent):
        self.frame = parent
        self.video_paths = []
        self.output_folder = 'output'
        self.worker = None
        self.fonts_folder = os.path.join(BASE_DIR, 'fonts')
        self.video_widgets = []

        self.init_ui()

    def init_ui(self):
        main_container = ctk.CTkFrame(self.frame, fg_color='transparent')
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # === Top Buttons ===
        top_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        top_frame.pack(fill="x", pady=(0, 15))

        self.top_buttons = [
            ['➕ Tambah Video', 'left', (0, 10), self.add_video],
            ['📁 Tambah Folder', 'left', (0, 10), self.add_folder],
            ['📂 Output Folder', 'right', (10, 10), self.select_output_folder],
            ['🚀 Mulai Batch Caption', 'right', None, self.start_batch_processing]
        ]

        for i in range(len(self.top_buttons)):
            button = ctk.CTkButton(
                top_frame, 
                text=self.top_buttons[i][0],
                height=40,
                command=self.top_buttons[i][3]
            )
            button.pack(side=self.top_buttons[i][1], padx=self.top_buttons[i][2])
        
        # === Video Table Section ===
        video_section = ctk.CTkFrame(main_container, fg_color='transparent')
        video_section.pack(fill='both', expand=True, pady=(0, 15))

        video_label = ctk.CTkLabel(
            video_section,
            text="Video",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#8a8a9a"
        )
        video_label.pack(anchor="w", pady=(0, 5))

        self.video_scroll = ctk.CTkScrollableFrame(video_section, height=200)
        self.video_scroll.pack(fill="both", expand=True)

        # === Caption Style Section ===
        style_section = ctk.CTkFrame(main_container, fg_color="transparent")
        style_section.pack(fill="x", pady=(0, 15))

        style_label = ctk.CTkLabel(
            style_section,
            text="Caption Style",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#8a8a9a"
        )
        style_label.pack(anchor="w", pady=(0, 10))
        
        # 2x2 Grid Layout
        grid_frame = ctk.CTkFrame(style_section, fg_color="transparent")
        grid_frame.pack(fill="x")

        # Row 1: Style Pack | Accent Color
        row1 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 10))

        # Style Pack (Left)
        style_pack_frame = ctk.CTkFrame(row1, fg_color="transparent")
        style_pack_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        style_pack_label = ctk.CTkLabel(
            style_pack_frame,
            text="Style Pack",
            width=100,
            anchor="w"
        )
        style_pack_label.pack(side="left", padx=(0, 10))

        self.style_combo = ctk.CTkComboBox(
            style_pack_frame,
            values=["CapCut Pop", "Classic", "Modern", "Minimal"],
            width=250
        )
        self.style_combo.set("CapCut Pop")
        self.style_combo.pack(side="left")

        # Accent Color (Right)
        color_frame = ctk.CTkFrame(row1, fg_color="transparent")
        color_frame.pack(side="left", fill="x", expand=True)

        color_label = ctk.CTkLabel(
            color_frame,
            text="Accent Color",
            width=100,
            anchor="w"
        )
        color_label.pack(side="left", padx=(0, 10))

        self.color_input = ctk.CTkEntry(color_frame, width=200)
        self.color_input.insert(0, '#ff583a')
        self.color_input.pack(side='left', padx=(0, 10))

        btn_color_picker = ctk.CTkButton(
            color_frame,
            text='🎨',
            width=50,
            command=self.pick_color
        )
        btn_color_picker.pack(side='left')

        # Row 2: Mode | Font
        row2 = ctk.CTkFrame(grid_frame, fg_color='transparent')
        row2.pack(fill="x")

        # Mode (Left)
        mode_frame = ctk.CTkFrame(row2, fg_color='transparent')
        mode_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        mode_label = ctk.CTkLabel(
            mode_frame,
            text="Mode",
            width=100,
            anchor="w"
        )
        mode_label.pack(side="left", padx=(0, 10))

        self.mode_combo = ctk.CTkComboBox(
            mode_frame,
            values=["Word Accent", "Full Sentence", "Line by Line"],
            width=250
        )
        self.mode_combo.set("Word Accent")
        self.mode_combo.pack(side="left")

        # Font (Right)
        font_frame = ctk.CTkFrame(row2, fg_color="transparent")
        font_frame.pack(side="left", fill="x", expand=True)

        font_label = ctk.CTkLabel(
            font_frame,
            text="Font",
            width=100,
            anchor="w"
        )
        font_label.pack(side="left", padx=(0, 10))

        self.font_combo = ctk.CTkComboBox(
            font_frame,
            values=self._get_font_list(),
            width=250
        )
        self.font_combo.set("Default")
        self.font_combo.pack(side="left")

        # === Bottom Progress & Log ===
        bottom_section = ctk.CTkFrame(main_container, fg_color="transparent")
        bottom_section.pack(fill="x")

        progress_container = ctk.CTkFrame(bottom_section, fg_color="transparent")
        progress_container.pack(side="left", fill="x", expand=True)

        progress_label = ctk.CTkLabel(
            progress_container,
            text="Progress",
            font=ctk.CTkFont(size=12),
            text_color="#8a8a9a"
        )
        progress_label.pack(anchor="w")
        
        self.progress_bar = ctk.CTkProgressBar(progress_container)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(5, 5))
        
        self.progress_status = ctk.CTkLabel(
            progress_container,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color="#8a8a9a"
        )
        self.progress_status.pack(anchor="w")
        
        btn_export_log = ctk.CTkButton(
            bottom_section,
            text="📄 Export Log",
            width=150,
            command=self.export_log
        )
        btn_export_log.pack(side="right", padx=(10, 0))
    
    def _create_option_row(self, parent, label_text, widget_type, values=None, var_name=None):
        """Helper to create consistent option rows"""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=(0, 10))
        
        label = ctk.CTkLabel(row, text=label_text, width=120, anchor="w")
        label.pack(side="left", padx=(0, 10))
        
        if widget_type == "combo":
            widget = ctk.CTkComboBox(row, values=values, width=400)
            widget.set(values[0])
        
        widget.pack(side="left")
        
        if var_name:
            setattr(self, var_name, widget)
        
        return widget
    
    def _get_font_list(self):
        """Get list of fonts from fonts folder"""
        fonts = ["Default"]
        if os.path.exists(self.fonts_folder):
            for file in os.listdir(self.fonts_folder):
                if file.lower().endswith(('.ttf', '.otf')):
                    fonts.append(file)
        return fonts
    
    def add_video(self):
        files = filedialog.askopenfilenames(
            title="Select Videos",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
        )
        if files:
            for file in files:
                if file not in self.video_paths:
                    self.video_paths.append(file)
            self.update_video_list()
    
    def add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            for file in os.listdir(folder):
                if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    full_path = os.path.join(folder, file)
                    if full_path not in self.video_paths:
                        self.video_paths.append(full_path)
            self.update_video_list()
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            messagebox.showinfo("Output Folder", f"Output folder set to:\n{folder}")
    
    def pick_color(self):
        color = colorchooser.askcolor(title="Choose Accent Color")
        if color[1]:
            self.color_input.delete(0, tk.END)
            self.color_input.insert(0, color[1])
    
    def update_video_list(self):
        # Clear existing widgets
        for widget_dict in self.video_widgets:
            widget_dict['frame'].destroy()
        self.video_widgets.clear()
        
        # Create new video rows
        for idx, path in enumerate(self.video_paths):
            filename = os.path.basename(path)
            
            # Container for each video row
            row_frame = ctk.CTkFrame(self.video_scroll)
            row_frame.pack(fill="x", pady=5, padx=5)
            
            # Filename label
            name_label = ctk.CTkLabel(
                row_frame,
                text=filename,
                anchor="w"
            )
            name_label.pack(side="left", fill="x", expand=True, padx=(10, 10))
            
            # Progress bar
            progress = ctk.CTkProgressBar(row_frame, width=150)
            progress.set(0)
            progress.pack(side="left", padx=(0, 10))

            # Remove button
            btn_remove = ctk.CTkButton(
                row_frame,
                text="Remove",
                width=80,
                command=lambda p=path: self.remove_video(p)
            )
            btn_remove.pack(side="left", padx=(0, 10))

            # Store references
            self.video_widgets.append({
                'frame': row_frame,
                'path': path,
                'progress': progress,
                'label': name_label
            })
    
    def remove_video(self, path):
        if path in self.video_paths:
            self.video_paths.remove(path)
            self.update_video_list()
    
    def start_batch_processing(self):
        if not self.video_paths:
            messagebox.showwarning("No Videos", "Please add videos first!")
            return
        
        if self.worker and self.worker.isRunning():
            messagebox.showwarning("Processing", "Already processing videos!")
            return
        
        selected_font = self.font_combo.get()
        font_path = None
        if selected_font != "Default":
            font_path = os.path.join(self.fonts_folder, selected_font)
        
        self.progress_bar.set(0)
        self.progress_status.configure(text="Starting...")
        
        # self.worker = CaptionWorker(
        #     video_paths=self.video_paths,
        #     style_pack=self.style_combo.get(),
        #     mode=self.mode_combo.get(),
        #     accent_color=self.color_input.get(),
        #     override_font=font_path,
        #     output_folder=self.output_folder
        # )
        
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_progress(self, value, message):
        self.progress_bar.set(value / 100)
        self.progress_status.configure(text=message)
    
    def on_finished(self):
        messagebox.showinfo("Complete", "All videos processed successfully!")
        self.progress_status.configure(text='Completed')
    
    def on_error(self, error_msg):
        messagebox.showerror("Error", f"An error occurred:\n{error_msg}")
        self.progress_status.configure(text=f'Error: {error_msg}')
    
    def export_log(self):
        popup = CTkToplevel(self.frame)
        popup.title("Export Log")
        popup.geometry("300x150")
        popup.resizable(False, False)

        # Center the popup on the parent
        popup.update_idletasks()
        x = self.frame.winfo_x() + (self.frame.winfo_width() // 2) - (300 // 2)
        y = self.frame.winfo_y() + (self.frame.winfo_height() // 2) - (150 // 2)
        popup.geometry(f"+{x}+{y}")

        # Label text
        label = ctk.CTkLabel(
            popup,
            text='Log export feature coming soon!',
            wraplength=250,
            font=ctk.CTkFont(size=14, weight='normal')
        )
        label.pack(pady=20, padx=20)

        # Close button
        close_btn = ctk.CTkButton(popup, text="OK", width=80, command=popup.destroy)
        close_btn.pack(pady=10)

        # Make sure the popup is modal (block interaction with main window)
        popup.grab_set()
