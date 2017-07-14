# The 2013 Steam release of SNA3D is the same as 1994 version
# but with a newer copyright.

noah = importlib.import_module('.a2315a14', 'extractor.roms')

def init(rom):
    noah.init(rom)
    rom.rom_name = "Super Noah's Ark 3D (2013)"
