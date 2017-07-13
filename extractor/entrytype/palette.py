from entry import Entry
from ..utils import *

class Palette(Entry):
    colors = None
    # Constants
    _DATA_LENGTH = 0x200

    '''
    Constructor.
    Reads a palette from the current position within a file.
    The palette is converted from 15-bit colors to 32-bit RGBA tuples.
    '''
    def __init__(self, rom, name):
        Entry.__init__(self, rom, name)
        self.colors = [Palette.convert_15bit_to_rgba(read_ushort(rom)) for x in range(256)]

    '''
    Converts a 15-bit color to a 32-bit RGBA tuple for use in the palette for PNG file creation.
    FF 7F => 255,255,255
    '''
    @staticmethod
    def convert_15bit_to_rgba(color):
        r = ((color) % 32) * 8
        g = ((color >> 5) % 32) * 8
        b = ((color >> 10) % 32) * 8
        a = 0xff
        return (r, g, b, a)

    '''
    Gets the data length of a palette.
    This is the length of data read from the rom.
    '''
    @staticmethod
    def get_data_length():
        return Palette._DATA_LENGTH

    '''
    Converts an 24-bit RGB or 32-bit RGBA color to 15-bit.
    255,255,255 => MSB: 0,11111,11 111,11111 LSB => FF 7F
    '''
    @staticmethod
    def convert_rgb_to_15_bit(color):
        return (color[0] / 8) | ((color[1] / 8) << 5) + ((color[2] / 8) << 10)

    '''
    Saves a palette to the given filename.
    The given palette can be RGB or RGBA.
    The palette file is a simple byte dump of the palette in 24-bit RGB.
    '''
    def save(self, filename):
        with open(filename, "wb") as f:
            # Write RGB values, trim off Alpha.
            f.write(str(bytearray([x for y in [z[0:3] for z in self.colors] for x in y])))

    '''
    Returns the default file extension to use while saving.
    Should be with the period.
    '''
    def get_default_extension(self):
        return ".pal"
