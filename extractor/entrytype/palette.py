from . import AbstractEntry

class Palette(AbstractEntry):
    """Reads a SNES style 15-bit palette and converts to it a 32-bit
    RGBA palette.
    """
    # Constants
    _DATA_LENGTH = 0x200

    def __init__(self, offset, name):
        AbstractEntry.__init__(self, offset, name)
        self.colors = None

    def load(self, rom):
        # Check that the palette
        if self.colors is None:
            rom.seek(self.offset)
            self.colors = [Palette.convert_15bit_to_rgba(rom.read_ushort()) for x in range(256)]

    def save(self, path, filename=None, filetype=None):
        """Saves the palette data as a 24-bit RGB byte dump."""
        filename = self._get_filename(path, filename, self.name + '.pal')
        with open(filename, "wb") as f:
            # Write RGB values, trim off Alpha.
            f.write(str(bytearray([x for y in [z[0:3] for z in self.colors] for x in y])))

    def _get_length(self):
        return Palette._DATA_LENGTH

    @staticmethod
    def convert_15bit_to_rgba(color):
        """Converts a 15-bit color to a 32-bit RGBA tuple for use as the
        palette for PNG file creation.
        
        ex: FF 7F => 255,255,255
        """
        r = ((color) % 32) * 8
        g = ((color >> 5) % 32) * 8
        b = ((color >> 10) % 32) * 8
        a = 0xff
        return (r, g, b, a)

    @staticmethod
    def convert_rgb_to_15_bit(color):
        """Converts an 24-bit RGB or 32-bit RGBA color to 15-bit.

        ex: 255,255,255 => MSB: 0,11111,11 111,11111 LSB => FF 7F
        """
        return (color[0] / 8) | ((color[1] / 8) << 5) + ((color[2] / 8) << 10)
