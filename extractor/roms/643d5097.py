# The 2013 Steam release of SNA3D is the same as 1994 version
# but with a newer copyright.
from . import noah3d as base

def init(rom):
    base._rom_name = "Super 3D Noah's Ark (2013)"
    base.init(rom)
