import inspect
import json
import os
import Tkinter as tk
if __name__ == "__main__":
    # Sloppy hack to get the relative import to work when running this as main without using -m flag.
    import sys
    sys.path.append('../..')
from extractor.entrytype import *

class Settings():
    # TODO Use AppData path for config file?
    CONFIG_FILE = 'config.json'

    def __init__(self):
        self.rom_file = tk.StringVar()
        self.export_folder = tk.StringVar(value=os.getcwd())
        self.export_to_subfolder = tk.BooleanVar(value=True)
        self.combine_maps = tk.BooleanVar(value=True)
        self.export = dict([(key,tk.IntVar(value=1)) for key in Settings.get_export_types()])
        self.load()

    def load(self):
        if os.path.exists(Settings.CONFIG_FILE):
            with open(Settings.CONFIG_FILE, 'r') as f:
                self.from_dict(json.load(f))

    def save(self):
        with open(Settings.CONFIG_FILE, 'w') as f:
            json.dump(self.to_dict(), f, indent=4, separators=(',', ': '))

    def to_dict(self):
        settings = {
            'rom_file': self.rom_file.get(),
            'export_folder': self.export_folder.get(),
            'export_to_subfolder': self.export_to_subfolder.get(),
            'combine_maps': self.combine_maps.get(),
            }
        settings['export'] = {key:value.get() for key, value in self.export.items()}
        return settings

    def from_dict(self, settings):
        # Be sure to use .set so that the only variable value updates and the variable reference doesn't change.
        self.rom_file.set(settings.get('rom_file', ''))
        if not os.path.isfile(self.rom_file.get()):
            self.rom_file.set('')
        self.export_folder.set(settings.get('export_folder', os.getcwd()))
        if not os.path.isdir(self.export_folder.get()):
            self.export_folder.set(os.getcwd())
        self.export_to_subfolder.set(settings.get('export_to_subfolder', True))
        self.combine_maps.set(settings.get('combine_maps', True))
        export = settings.get('export', {})
        for key in Settings.get_export_types():
            self.export[key].set(export.get(key, 1))

    @staticmethod
    def get_export_types():
        cls = list({name for name, cls in globals().items() if inspect.isclass(cls) and cls != AbstractEntry and issubclass(cls, AbstractEntry)})
        cls.sort()
        return cls

    def get_export_class_list(self):
        cls = [globals()[key] for key,value in self.export.items() if value.get() == 1]
        cls.sort()
        return cls

# For testing.
if __name__ == "__main__":
    def callback(*args):
        print 'Trace callback: ',
        print args

    root = tk.Tk()
    print "get_export_types: "
    print Settings.get_export_types()
    print
    settings = Settings()
    settings.rom_file.trace('w', callback)
    settings.export['Sprite'].trace('w', callback)
    settings.from_dict({'rom_file':'folder/file.sfc', 'export': {'Sprite': 0}})
    print "json encode: "
    print json.JSONEncoder(indent=4, separators=(',', ': ')).encode(settings.to_dict())
    print ""
    print settings.to_dict()
