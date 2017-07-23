import Tkinter as tk
from .romframe import RomFrame
from .optionsframe import OptionsFrame
from .settings import Settings

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # Set up the window.
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.settings = Settings()
        # Widget creation.
        self.rom_frame = RomFrame(self)
        self.options_frame = OptionsFrame(self)
        # Perform layout.
        self.rom_frame.pack(fill=tk.X)
        self.options_frame.pack(fill=tk.X)
        self.pad_children(self, 5)
        # Load settings.
        self.rom_frame.load_settings(self.settings)
##        self.rom_frame.set_rom_file(self.settings.rom_file)
##        self.options_frame.set_settings(self.settings.export)

    def on_closing(self):
        self.settings.save()
        self.parent.destroy()

    def pad_children(self, parent, pad):
        for widget in parent.winfo_children():
            widget.grid(padx=pad, pady=pad)
