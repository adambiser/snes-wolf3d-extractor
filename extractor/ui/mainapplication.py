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
        # Add widgets
        pad = {'padx':5, 'pady':5}
        RomFrame(self,
                 self.settings
                 ).pack(anchor=tk.NW,
                        fill=tk.X,
                        **pad
                        )
        OptionsFrame(self,
                     self.settings
                     ).pack(anchor=tk.NW,
                            fill=tk.X,
                            **pad
                            )
        self.minsize(500, 400)
        self.center_window(500, 400)

    def on_closing(self):
        self.settings.save()
        self.destroy()

    def center_window(self, width, height):
        x = (self.winfo_screenwidth() - width) / 2
        y = (self.winfo_screenheight() - height) / 2
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
