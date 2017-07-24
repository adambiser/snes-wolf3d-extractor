import os
import Tkinter as tk
import tkMessageBox
from tkFileDialog import askdirectory
from romframe import RomFrame
from optionsframe import OptionsFrame
from settings import Settings
from statustext import StatusText
from extractor.rom import Rom
from extractor.entrytype import *

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
##        self.status = StatusText(self,
####                              state=tk.DISABLED,
##                              )
##        self.status.pack(anchor=tk.NW,
##                         fill=tk.BOTH,
##                         expand=1,
##                         **pad
##                         )
##        for x in range(10):
##            self.status.appendline('test {}'.format(x))
##        self.status.config(state=tk.DISABLED)
        tk.Button(self,
                  text='Export',
                  name='export_button',
                  command=self.export,
                  ).pack(fill=tk.X,
                         **pad
                         )
        self.minsize(500, 220)
        self.center_window(500, 220)
        # Force this code to run.
        self.on_rom_valid_changed()

    def on_rom_valid_changed(self, *args):
        enabled = self.children['rom_frame'].is_rom_valid.get()
        self.children['export_button'].config(state = tk.NORMAL if enabled else tk.DISABLED)

    def on_closing(self):
        self.settings.save()
        self.destroy()

    def center_window(self, width, height):
        x = (self.winfo_screenwidth() - width) / 2
        y = (self.winfo_screenheight() - height) / 2
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def export(self):
        folder = askdirectory(title='Choose output directory.\nThe files will appear in a subfolder.',
                              initialdir=self.settings.output_folder.get(),
                              mustexist=1,
                              parent=self,
                              )
        if not folder:
            return
        if os.listdir(folder):
            print 'Export folder not empty.'
            if not tkMessageBox.askyesno('Confirmation', 'The folder does not appear to be empty. Continue?'):
                print 'Aborted.'
                return
            print 'Confirmed.'
        print 'Exporting to: ' + folder
        self.config(cursor='wait')
        self.settings.output_folder.set(folder)
        export_classes = self.settings.get_export_class_list()
        with Rom(self.settings.rom_file.get()) as rom:
            # Save maps in a single file.
            if Map in export_classes:
                gamemaps = [rom.get_entry(m).generate_dos_map() for m in rom.get_entries_of_class(Map)]
                Map.save_as_wdc_map_file(folder + "/snes.map", gamemaps)
            for index in range(rom.get_entry_count()):
                if rom.get_entry_type(index) is Map:
                    continue
                if rom.get_entry_type(index) in export_classes:
                    entry = rom.get_entry(index)
                    print '0x{:x} - {}'.format(entry.offset, entry.name)
                    entry.save(folder)
        self.config(cursor='')
