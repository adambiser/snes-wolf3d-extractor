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
        self.load()

    def load(self):
        settings = {}
        if os.path.exists(Settings.CONFIG_FILE):
            with open(Settings.CONFIG_FILE, 'r') as f:
                settings = json.load(f)
        self.from_dict(settings)

    def save(self):
        with open(Settings.CONFIG_FILE, 'w') as f:
            json.dump(self.to_dict(), f, indent=4, separators=(',', ': '))

    def to_dict(self):
        settings = { 'rom_file': self.rom_file }
        settings['export'] = {key:value.get() if isinstance(value, tk.IntVar) else value for key, value in self.export.items()}
        return settings

    def from_dict(self, settings):
        self.rom_file = settings.get('rom_file', '')
        export = settings.get('export', {})
        self.export = dict([(key,tk.IntVar(value=export.get(key, 1))) for key in Settings.get_export_types()])

    @staticmethod
    def get_export_types():
        cls = list({name for name, cls in globals().items() if inspect.isclass(cls) and cls != AbstractEntry and issubclass(cls, AbstractEntry)})
        cls.sort()
        return cls

# For testing.
if __name__ == "__main__":
    root = tk.Tk()
    print "get_export_types: "
    print Settings.get_export_types()
    print
    settings = Settings()
    settings.from_dict({'rom_file':'folder/file.sfc', 'export': {'Sprite': 0}})
    print "json encode: "
    print json.JSONEncoder(indent=4, separators=(',', ': ')).encode(settings.to_dict())
    print ""
    print settings.to_dict()
