import os
import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askdirectory

from . import utils as ui_utils
from .optionsframe import OptionsFrame
from .romframe import RomFrame
from .settings import Settings
from .statustext import StatusText
from .. import utils
from ..entrytype import *
from ..rom import Rom


class MainApplication(tk.Tk):
    # noinspection PyPep8Naming
    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1):
        # Set up the window.
        super().__init__(screenName, baseName, className, useTk)
        self.title('SNES Wolfenstein 3D Extractor')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.settings = Settings()
        # Add widgets
        pad = {'padx': 5, 'pady': 5}
        RomFrame(self,
                 self.settings,
                 name='rom_frame',
                 ).pack(anchor=tk.NW,
                        fill=tk.X,
                        **pad
                        )
        self.children['rom_frame'].is_rom_valid.trace("w", self.on_rom_valid_changed)
        OptionsFrame(self,
                     self.settings
                     ).pack(anchor=tk.NW,
                            fill=tk.X,
                            **pad
                            )
        self.status = StatusText(self)
        self.status.pack(anchor=tk.NW,
                         fill=tk.BOTH,
                         expand=True,
                         **pad
                         )
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.BOTTOM,
                               fill=tk.X,
                               )
        self.button_frame.grid_columnconfigure(0, weight=1, uniform='x')
        self.button_frame.grid_columnconfigure(1, weight=1, uniform='x')
        tk.Button(self.button_frame,
                  text='Export',
                  name='export_button',
                  command=self.export,
                  ).grid(row=0,
                         column=0,
                         sticky=tk.W+tk.E,
                         **pad
                         )
        tk.Button(self.button_frame,
                  text='Open Current Export Folder',
                  command=self.open_export_folder,
                  ).grid(row=0,
                         column=1,
                         sticky=tk.W+tk.E,
                         **pad
                         )
        self.minsize(600, 500)
        ui_utils.center_window(self, 600, 500)
        # Force this code to run.
        self.on_rom_valid_changed()

    # noinspection PyUnusedLocal
    def on_rom_valid_changed(self, *args):
        enabled = self.children['rom_frame'].is_rom_valid.get()
        self.button_frame.children['export_button'].config(state=tk.NORMAL if enabled else tk.DISABLED)

    def on_closing(self):
        self.settings.save()
        self.destroy()

    def add_status(self, status_text):
        self.status.appendline(status_text)
        self.update()

    def open_export_folder(self):
        os.startfile(self.settings.export_folder.get())

    def export(self):
        folder = askdirectory(title='Choose output directory.\nThe files will appear in a subfolder.',
                              initialdir=self.settings.export_folder.get(),
                              mustexist=True,
                              parent=self,
                              )
        if not folder:
            return
        with Rom(self.settings.rom_file.get()) as rom:
            export_folder = folder
            if self.settings.export_to_subfolder.get():
                export_folder = os.path.join(export_folder, rom.name)
                utils.create_path(export_folder)
            self.add_status('Exporting to: ' + export_folder)
            if os.listdir(export_folder):
                self.add_status('Export folder not empty.')
                if not tkinter.messagebox.askyesno('Confirmation', 'The folder does not appear to be empty.\n'
                                                                   'Existing files may be overwritten.\nContinue?'):
                    self.add_status('Aborted.')
                    return
                self.add_status('Confirmed.')
            try:
                self.config(cursor='wait')
                # Save folder without generated subfolder.
                self.settings.export_folder.set(folder)
                export_classes = self.settings.get_export_class_list()
                # Save maps in a single file.
                if self.settings.combine_maps.get() and Map in export_classes:
                    gamemaps = [rom.get_entry(m).generate_dos_map() for m in rom.get_entries_of_class(Map)]
                    self.add_status(f'Exporting: {len(gamemaps)} maps to Maps.map')
                    Map.save_as_wdc_map_file(export_folder + "/Maps.map", gamemaps)
                for index in range(rom.get_entry_count()):
                    if rom.get_entry_type(index) in export_classes:
                        if rom.get_entry_type(index) is Map and self.settings.combine_maps.get():
                            continue
                        entry = rom.get_entry(index)
                        self.add_status('Exporting: 0x{:x} - {}'.format(entry.offset, entry.name))
                        entry.save(export_folder)
            finally:
                self.config(cursor='')
        self.add_status('Done')
