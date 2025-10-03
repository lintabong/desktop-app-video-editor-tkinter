import customtkinter as ctk
from tkinter import filedialog, messagebox

def show_export_log_popup(frame, title, log_text):
    popup = ctk.CTkToplevel(frame)
    popup.title(title)
    popup.geometry("300x180")
    popup.resizable(False, False)

    popup.update_idletasks()
    x = frame.winfo_x() + (frame.winfo_width() // 2) - (300 // 2)
    y = frame.winfo_y() + (frame.winfo_height() // 2) - (180 // 2)
    popup.geometry(f"+{x}+{y}")

    label = ctk.CTkLabel(
        popup,
        text="Do you want to export the log to a file?",
        wraplength=250,
        font=ctk.CTkFont(size=14)
    )
    label.pack(pady=20, padx=20)


    # Close button
    close_btn = ctk.CTkButton(popup, text="OK", width=80, command=popup.destroy)
    close_btn.pack(pady=10)

    # Make sure the popup is modal (block interaction with main window)
    popup.grab_set()