import Tkinter as tk
from tkFileDialog import askopenfilename

##class Event():
##    def __init__(self, source, **attrs):
##        self.source = source
##        for k, v in attrs.iteritems():
##            setattr(self, k, v)

# From:
# https://stackoverflow.com/questions/1092531/event-system-in-python/2022629#2022629
##class Callbacks(list):
##    def __call__(self, *args, **kwargs):
##        for func in self:
##            func(*args, **kwargs)
##
##    def __repr__(self):
##        return "Event(%s)" % list.__repr__(self)

class RomFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # Settings
##        self.callbacks = Callbacks()
##        self.callbacks.append(self.test)
        self.rom_file = tk.StringVar()
        # Widget creation.
        self.rom_label = tk.Label(self, text='ROM:')
        self.rom_file_label = tk.Label(self, textvariable=self.rom_file, width=60, borderwidth=1, relief=tk.SUNKEN, anchor=tk.W)
        self.select_rom_button = tk.Button(self, text='Select ROM', command=self.select_rom)
        # Perform layout.
        self.rom_label.grid(row=0, column=0, sticky=tk.W)
        self.rom_file_label.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.select_rom_button.grid(row=0, column=2, sticky=tk.E)
        tk.Grid.columnconfigure(self, 1, weight=1)

    def select_rom(self):
        self.set_rom_file(askopenfilename(
            initialdir=self.rom_file.get(),
            title='Select ROM',
            filetypes =(('ROM files', '*.sfc;*.smc'), ('All files', '*.*')),
            ))

    def set_rom_file(self, rom_file):
        if rom_file == '':
            return
        self.rom_file.set(rom_file)
##        self.fire(name=rom_file)
##        self.callbacks([1,2], name=rom_file)

    def load_settings(self, settings):
        self.set_rom_file(settings.rom_file)

##    def test(self, *args, **kwargs):
##        print args
##        print kwargs

##    def subscribe(self, callback):
##        self.callbacks.append(callback)
##
##    def fire(self, **attrs):
##        e = Event(self, **attrs)
##        print e.name
##        for func in self.callbacks:
##            func(e)
