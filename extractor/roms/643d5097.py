# The 2013 Steam release of SNA3D is the same as 1994 version
# but with a newer copyright.
import importlib
base = importlib.import_module('.a2315a14', 'extractor.roms')

def init(rom):
    base._rom_name = "Super 3D Noah's Ark (2013)"
    base.init(rom)
