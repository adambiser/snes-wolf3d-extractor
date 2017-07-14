from . import a2315a14 as noah

# The 2013 Steam release of SNA3D is the same as 1994 version
# but with a newer copyright.

def init(rom):
    noah.init(rom)
    rom.rom_name = "Super Noah's Ark 3D (2013)"
