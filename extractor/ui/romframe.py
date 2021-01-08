import os
import tkinter as tk
from tkinter.filedialog import askopenfilename

from ..exceptions import RomInfoNotFoundError
from ..rom import Rom
from .entrylisttoplevel import EntryListTopLevel


class RomFrame(tk.Frame):
    def __init__(self, parent, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.settings = settings
        self.settings.rom_file.trace("w", self.rom_changed)
        self.rom_name = tk.StringVar()
        self.rom_info = tk.StringVar()
        self.rom_crc32 = tk.StringVar()
        self.entry_count = tk.IntVar()
        self.is_rom_valid = tk.BooleanVar(False)
        # Add widgets.
        # Row 0
        tk.Label(self,
                 text='ROM:',
                 ).grid(row=0,
                        column=0,
                        sticky=tk.W,
                        )
        tk.Label(self,
                 textvariable=self.settings.rom_file,
                 width=60,
                 borderwidth=1,
                 relief=tk.SUNKEN,
                 anchor=tk.W,
                 ).grid(row=0,
                        column=1,
                        columnspan=3,
                        sticky=tk.W+tk.E,
                        padx=(5, 5),
                        )
        tk.Button(self,
                  text='Select',
                  command=self.select_rom,
                  ).grid(row=0,
                         column=4,
                         sticky=tk.W+tk.E,
                         )
        # Row 1
        tk.Label(self,
                 text='Name:',
                 ).grid(row=1,
                        column=0,
                        sticky=tk.W,
                        )
        tk.Label(self,
                 textvariable=self.rom_name,
                 name='rom_name_label',
                 anchor=tk.W,
                 ).grid(row=1,
                        column=1,
                        columnspan=4,
                        sticky=tk.W+tk.E,
                        padx=(5, 0),
                        )
        # Row 2
        tk.Label(self,
                 text='CRC32:',
                 ).grid(row=2,
                        column=0,
                        sticky=tk.W,
                        )
        tk.Label(self,
                 textvariable=self.rom_crc32,
                 anchor=tk.W,
                 ).grid(row=2,
                        column=1,
                        sticky=tk.W+tk.E,
                        padx=5,
                        )
        tk.Label(self,
                 text='Entries:',
                 ).grid(row=2,
                        column=2,
                        sticky=tk.W,
                        )
        tk.Label(self,
                 textvariable=self.entry_count,
                 anchor=tk.W,
                 ).grid(row=2,
                        column=3,
                        sticky=tk.W+tk.E,
                        padx=5,
                        )
        tk.Button(self,
                  name='view_entry_list_button',
                  text='View',
                  state=tk.DISABLED,
                  command=self.show_entry_list,
                  ).grid(row=2,
                         column=4,
                         sticky=tk.W+tk.E,
                         )
        # Row 3
        tk.Label(self,
                 text='Info:',
                 ).grid(row=3,
                        column=0,
                        sticky=tk.W,
                        )
        tk.Label(self,
                 textvariable=self.rom_info,
                 anchor=tk.W,
                 ).grid(row=3,
                        column=1,
                        columnspan=4,
                        sticky=tk.W+tk.E,
                        padx=(5, 0),
                        )
        # lb_frame = tk.Frame(self)
        # lb_scrollbar = tk.Scrollbar(lb_frame, orient=tk.VERTICAL)
        # self.entry_listbox = tk.Listbox(lb_frame, yscrollcommand=lb_scrollbar.set)
        # lb_scrollbar.config(command=self.entry_listbox.yview)
        # lb_frame.grid(row=1, column=0, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S, pady=5)
        # lb_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # self.entry_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        tk.Grid.columnconfigure(self, 0, uniform='a')
        tk.Grid.columnconfigure(self, 2, uniform='a')
        tk.Grid.columnconfigure(self, 1, weight=1, uniform='b')
        tk.Grid.columnconfigure(self, 3, weight=1, uniform='b')
        # tk.Grid.rowconfigure(self, 1, weight=1)
        # Force this code to happen.
        self.rom_changed()

    def select_rom(self):
        initialdir, initialfile = os.path.split(self.settings.rom_file.get())
        rom_file = askopenfilename(
            initialdir=initialdir,
            initialfile=initialfile,
            title='Select ROM',
            filetypes=(('ROM files', '*.sfc;*.smc'), ('All files', '*.*')),
            )
        if not rom_file:
            return
        self.settings.rom_file.set(rom_file)

    def show_entry_list(self):
        EntryListTopLevel(self, self.settings.rom_file.get())

    # noinspection PyUnusedLocal
    def rom_changed(self, *args):
        rom_name_label = self.children['rom_name_label']
        rom_file = self.settings.rom_file.get()
        if not rom_file:
            return
        try:
            with Rom(rom_file) as rom:
                self.rom_name.set(rom.name)
                self.rom_info.set(rom.info + ((', ' if len(rom.info) > 0 else '') +
                                              'Data offset: 0x{:x}'.format(rom.offset_delta) if rom.offset_delta > 0
                                              else ''))
                rom_name_label['background'] = self['background']
                self.rom_crc32.set(rom.datacrc32 + ("File: " + rom.filecrc32 if rom.filecrc32 != rom.filecrc32 else ""))
                self.entry_count.set(rom.get_entry_count())
                self.children['view_entry_list_button'].config(state=tk.NORMAL)
                self.is_rom_valid.set(True)
        except RomInfoNotFoundError as e:
            print(f'Could not detect ROM: {e.crc32}')
            self.rom_name.set('Could not find ROM information.')
            self.rom_info.set('')
            rom_name_label['background'] = 'red'
            self.rom_crc32.set(e.crc32)
            self.entry_count.set(0)
            self.children['view_entry_list_button'].config(state=tk.DISABLED)
            self.is_rom_valid.set(False)
