import Tkinter as tk
from tkFileDialog import askopenfilename

class RomFrame(tk.Frame):
    def __init__(self, parent, settings, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.settings = settings
        # Widget creation.
        self.rom_label = tk.Label(self, text='ROM:')
        self.rom_file_label = tk.Label(self, textvariable=self.settings.rom_file, width=60, borderwidth=1, relief=tk.SUNKEN, anchor=tk.W)
        self.select_rom_button = tk.Button(self, text='Select ROM', command=self.select_rom)
        # Perform layout.
        self.rom_label.grid(row=0, column=0, sticky=tk.W)
        self.rom_file_label.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5)
        self.select_rom_button.grid(row=0, column=2, sticky=tk.E)
        tk.Grid.columnconfigure(self, 1, weight=1)

    def select_rom(self):
        self.set_rom_file(askopenfilename(
            initialdir=self.settings.rom_file,
            title='Select ROM',
            filetypes =(('ROM files', '*.sfc;*.smc'), ('All files', '*.*')),
            ))

    def set_rom_file(self, rom_file):
        if rom_file == '':
            return
        self.settings.rom_file.set(rom_file)
