import customtkinter

class MultiVideoJoinerTab:
    def __init__(self, parent):
        self.frame = parent

        label = customtkinter.CTkLabel(self.frame, text="📽️ Multi Video Joiner", font=customtkinter.CTkFont(size=18, weight="bold"))
        label.pack(pady=20)

        run_button = customtkinter.CTkButton(self.frame, text="Join Videos", command=self.join_videos)
        run_button.pack(pady=10)

    def join_videos(self):
        print("[MultiVideoJoinerTab] Joining videos...")
