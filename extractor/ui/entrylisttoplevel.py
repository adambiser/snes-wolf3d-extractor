import os
import tkinter as tk

from . import utils as ui_utils
from .statustext import StatusText
from ..rom import Rom


class EntryListTopLevel(tk.Toplevel):
    def __init__(self, master=None, filename=None, **options):
        super().__init__(master, **options)
        self.wm_title('Entries in ' + os.path.basename(filename))
        self.minsize(400, 600)
        ui_utils.center_window(self, 400, 600)
        textbox = StatusText(self)
        textbox.config(text='Entries')
        textbox.pack(anchor=tk.NW,
                     fill=tk.BOTH,
                     expand=True,
                     padx=5,
                     pady=5,
                     )
        with Rom(filename) as rom:
            for entry in rom.get_entry_list():
                textbox.appendline('0x{:x} - {} - {}'.format(entry[0], entry[1], entry[2]))
        textbox.textbox.see('1.0')
        self.transient(master)
        self.grab_set()
