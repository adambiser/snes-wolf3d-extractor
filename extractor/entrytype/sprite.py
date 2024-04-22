from .image import Image

# Note that this is just a color index unused by both the original Wolfenstein 3D and Super Noah's Ark 3D sprites.
TRANSPARENCY_COLOR_INDEX = 239


class Sprite(Image):
    # Constants
    SPRITE_SIZE = 64

    def __init__(self, offset, name, column_count, palette_name):
        # Note: 0 is an invalid "Image" storage method.  This class overwrites load, so it's OK.
        super().__init__(offset, name, 0,
                         Sprite.SPRITE_SIZE,
                         Sprite.SPRITE_SIZE,
                         palette_name,
                         transparency_color_index=TRANSPARENCY_COLOR_INDEX)
        self._column_count = column_count
        self._pixels = None

    def load(self, rom):
        """Loads and converts sprite data into pixel data."""
        self._load_palette(rom)
        rom.seek(self.offset)
        # noinspection PyUnusedLocal
        pixels = [[self._transparency_color_index for x in range(self._width)] for y in range(self._height)]
        page_offset = (self.offset & 0xffff0000)
        pixel_x = (self._width - self._column_count) // 2
        for line in range(self._column_count):
            rom.seek(self.offset + line * 2)
            line_offset = page_offset + rom.read_ushort()
            while True:
                rom.seek(line_offset)
                line_offset += 6
                top_y = rom.read_ushort()
                if top_y == 0xffff:
                    break
                top_y >>= 1
                bottom_y = rom.read_ushort() // 2
                pixel_offset = rom.read_ushort()
                rom.seek(page_offset + pixel_offset + top_y)
                for y in range(top_y, bottom_y):
                    pixels[y][pixel_x] = rom.read_ubyte()
            pixel_x += 1
        self._pixels = pixels
