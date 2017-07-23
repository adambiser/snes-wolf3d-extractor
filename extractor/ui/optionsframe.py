import Tkinter as tk

class OptionsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # Set up the window.
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.sprites = tk.IntVar(value=0)
        self.sprite_checkbox = tk.Checkbutton(self, text='Sprites', variable=self.sprites)
        self.sprite_checkbox.pack()

    def set_settings(self, settings):
        self.settings = settings
        self.sprites.set(1)
