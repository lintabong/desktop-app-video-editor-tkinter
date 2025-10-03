
import customtkinter
from ui.tabs.auto_video_mixer import AutoVideoMixerTab
from ui.tabs.auto_cutter_video import AutoCutterVideoTab
from ui.tabs.caption_ai import CaptionAiTab
from ui.tabs.multi_video_joiner import MultiVideoJoinerTab
from ui.tabs.clip_bot import ClipBotTab
from ui.tabs.settings import SettingsTab 

from utils import database

customtkinter.set_appearance_mode('Dark')
customtkinter.set_default_color_theme('green')  # green / blue / dark-blue


class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('🎬 Video Designer')

        # Create settings database
        database.init_config_db()

        # Desired window size
        app_width = 900
        app_height = 500

        # Get screen dimension to center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (app_width // 2)
        y = (screen_height // 2) - (app_height // 2)

        # 🪄 Set geometry and minimum size
        self.geometry(f'{app_width}x{app_height}+{x}+{y}')
        self.minsize(app_width, app_height)

        # Grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main tabview
        self.tabview = customtkinter.CTkTabview(self, width=850, height=800)
        self.tabview.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Tabs
        self.tabview.add('AIGC Auto Video Mixer')
        self.tabview.add('Auto Cutter Video')
        self.tabview.add('Caption AI')
        self.tabview.add('Multi Video Joiner')
        self.tabview.add('ClipBot')
        self.tabview.add('Settings') 

        # Attach contents
        AutoVideoMixerTab(self.tabview.tab('AIGC Auto Video Mixer'))
        AutoCutterVideoTab(self.tabview.tab('Auto Cutter Video'))
        CaptionAiTab(self.tabview.tab('Caption AI'))
        MultiVideoJoinerTab(self.tabview.tab('Multi Video Joiner'))
        ClipBotTab(self.tabview.tab('ClipBot'))
        SettingsTab(self.tabview.tab('Settings'))
