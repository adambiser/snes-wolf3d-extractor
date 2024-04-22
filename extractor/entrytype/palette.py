import png
import typing

from .abstractentry import AbstractEntry


class Palette(AbstractEntry):
    """Reads a SNES style 15-bit palette and converts to it a 32-bit RGBA palette."""
    # Constants
    _DATA_LENGTH = 0x200

    def __init__(self, offset, name):
        super().__init__(offset, name)
        self.colors = None

    def load(self, rom):
        # Check that the palette
        if self.colors is None:
            rom.seek(self.offset)
            self.colors = [Palette.convert_15bit_to_rgba(rom.read_ushort()) for _ in range(256)]

    def save(self, path, filename=None, filetype=None):
        """Saves the palette data as a 24-bit RGB byte dump."""
        pal_filename = self._get_filename(path, filename, self.name + '.pal')
        with open(pal_filename, "wb") as f:
            # Write RGB values, trim off Alpha.
            f.write(bytearray([x for y in [z[0:3] for z in self.colors] for x in y]))
        self.save_as_png(path, filename, filetype)

    def save_as_png(self, path, filename=None, filetype=None):
        # Save the palette as an 8-bit PNG.
        filename = self._get_filename(path, filename, self.name + '_pal.png')
        pixels = [[y * 16 + x for x in range(16)] for y in range(16)]
        with open(filename, 'wb') as f:
            w = png.Writer(len(pixels[0]), len(pixels), palette=self.colors, bitdepth=8)
            w.write(f, pixels)

    def _get_length(self):
        return Palette._DATA_LENGTH

    @staticmethod
    def convert_15bit_to_rgba(color: int):
        """Converts a 15-bit color to a 32-bit RGBA tuple for use as the palette for PNG file creation.
        
        ex: FF 7F => 255,255,255
        """
        r = (color % 32) * 8
        g = ((color >> 5) % 32) * 8
        b = ((color >> 10) % 32) * 8
        a = 0xff
        return r, g, b, a

    @staticmethod
    def convert_rgb_to_15_bit(color: typing.Tuple[int, ...]) -> int:
        """Converts an 24-bit RGB or 32-bit RGBA color to 15-bit.

        ex: 255,255,255 => MSB: 0,11111,11 111,11111 LSB => FF 7F
        """
        r, g, b, *_ = color
        return (r // 8) | ((g // 8) << 5) + ((b // 8) << 10)
