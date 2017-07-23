import inspect
import json
import os
import Tkinter as tk
if __name__ == "__main__":
    # Sloppy hack to get the relative import to work without using -m flag.
    import sys
    sys.path.append('../..')
    from extractor.entrytype import *
else:
    from ..entrytype import *

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
            json.dump(self.settings, f, indent=4, separators=(',', ': '))

    def to_dict(self):
        #if not key.startswith('__') and not callable(key)
        return {key:value.get() if isinstance(value, tk.IntVar) else value for key, value in self.__dict__.items()}

    def from_dict(self, settings):
        self.rom_file = settings.get('rom_file', '')
        self.export_sprites = tk.IntVar(value=settings.get('export_sprites', 1))

# For testing.
if __name__ == "__main__":
    root = tk.Tk()
    settings = Settings()
    settings.from_dict({'rom_file':'folder/file.sfc', 'export_sprites': 0})
    print json.JSONEncoder(indent=4, separators=(',', ': ')).encode(settings.to_dict())
    for cls in dir(): #[dir() if not cls.startswith('__')]:
        cls = globals()[cls]
        if inspect.isclass(cls) and (cls != AbstractEntry) and issubclass(cls, AbstractEntry):
            print cls.__name__
##    print settings.rom_file
##    print settings.export_sprites.get()
