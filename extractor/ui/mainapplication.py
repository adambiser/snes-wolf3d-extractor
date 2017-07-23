import Tkinter as tk
from .romframe import RomFrame
from .optionsframe import OptionsFrame
from .settings import Settings

class MainApplication(tk.Tk):
    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1):
        # Set up the window.
        tk.Tk.__init__(self, screenName, baseName, className, useTk)
        self.title('SNES Wolfenstein 3D Extractor')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.settings = Settings()
        # Widget creation.
        self.rom_frame = RomFrame(self, self.settings)
        self.options_frame = OptionsFrame(self)
        # Perform layout.
        pad = {'padx':5, 'pady':5}
        self.minsize(400, 100)
        self.rom_frame.pack(anchor=tk.NW, fill=tk.X, **pad)
        self.options_frame.pack(fill=tk.X, **pad)
##        self.pad_children(self, 5)

    def on_closing(self):
##        self.settings.save()
        self.destroy()

##    def pad_children(self, parent, pad):
##        for widget in parent.winfo_children():
##            widget.pack(padx=pad, pady=pad)
##            self.pad_children(widget, pad)
