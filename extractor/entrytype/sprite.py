from . import Image

class Sprite(Image):
    _column_count = None
    # Constants
    SPRITE_SIZE = 64

    def __init__(self, offset, name, column_count, palette_name):
        Image.__init__(self, offset, name, None, Sprite.SPRITE_SIZE, Sprite.SPRITE_SIZE, palette_name, transparency_color_index=0xff)
        self._column_count = column_count

    def load(self, rom):
        self._load_palette(rom)
        rom.seek(self.offset)
        """Loads and converts sprite data into pixel data."""
        pixels = [[self._transparency_color_index for x in range(self._width)] for y in range(self._height)]
        page_offset = (self.offset & 0xffff0000)
        pixel_x = (self._width - self._column_count) / 2
        for line in range(self._column_count):
            rom.seek(self.offset + line * 2)
            line_offset = page_offset + rom.read_ushort()
            while True:
                rom.seek(line_offset)
                line_offset += 6
                topY = rom.read_ushort()
                if topY == 0xffff:
                    break
                topY >>= 1
                bottomY = rom.read_ushort() / 2
                pixel_offset = rom.read_ushort()
                rom.seek(page_offset + pixel_offset + topY)
                for y in range(topY, bottomY):
                    pixels[y - 1][pixel_x] = rom.read_ubyte()
            pixel_x += 1
        self._pixels = pixels
