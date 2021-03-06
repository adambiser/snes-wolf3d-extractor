import struct
import typing

import png

from .abstractentry import AbstractEntry
if typing.TYPE_CHECKING:
    from ..rom import Rom


class Image(AbstractEntry):
    """Represents an image that is loaded from the rom.

    Uses PyPNG to save the image data to a png file.
    PyPNG is found at https://github.com/drj11/pypng
    """
    # Image storage method constants.
    LINEAR_8BIT = 1
    LINEAR_8BIT_RMO = 2  # Row Major Order
    TILED_8BIT = 3
    PLANAR_4BIT = 4
    PLANAR_8BIT = 5
    # Other constants
    _TILE_SIZE = 8

    def __init__(self, offset: int, name: str, storage_method: int, width: int, height: int, palette_name: str,
                 start_color_index: int = None, transparency_color_index: int = None):
        super().__init__(offset, name)
        self._storage_method = storage_method
        self._width = width
        self._height = height
        self._palette_name = palette_name
        self._palette_colors = None
        self._start_color_index = start_color_index
        self._transparency_color_index = transparency_color_index
        self._pixels = None

    def load(self, rom):
        self._load_palette(rom)
        rom.seek(self.offset)
        if self._storage_method == Image.LINEAR_8BIT:
            self._pixels = Image.get_linear_8bit(rom, self._width, self._height)
        elif self._storage_method == Image.LINEAR_8BIT_RMO:
            self._pixels = Image.get_linear_8bit_rmo(rom, self._width, self._height)
        elif self._storage_method == Image.TILED_8BIT:
            self._pixels = Image.get_tiled_8bit(rom, self._width, self._height)
        elif self._storage_method == Image.PLANAR_4BIT:
            self._pixels = Image.get_planar_4bit(rom, self._width, self._height, self._start_color_index)
        elif self._storage_method == Image.PLANAR_8BIT:
            self._pixels = Image.get_planar_8bit(rom, self._width, self._height)
        else:
            raise Exception(f'Image "{self.name}" was assigned an unknown storage method: {self._storage_method}')

    def save(self, path, filename=None, filetype=None):
        """Always saves the image with a bitdepth of 8, even if it is stored in the rom as 4-bit."""
        filename = self._get_filename(path, filename, self.name + '.png')
        with open(filename, 'wb') as f:
            w = png.Writer(len(self._pixels[0]), len(self._pixels), palette=self._palette_colors, bitdepth=8)
            w.write(f, self._pixels)

    def _load_palette(self, rom):
        # Load the palette, too.
        if self._palette_colors is None:
            palette = rom.get_entry(self._palette_name)
            # Clone the palette so changing the transparent color index doesn't change it in the original.
            self._palette_colors = palette.colors[:]
            if self._transparency_color_index is not None:
                self._palette_colors[self._transparency_color_index] = (0xff, 0xff, 0xff, 0)

    def _get_length(self):
        length = self._width * self._height
        if self._storage_method == Image.LINEAR_8BIT:
            return length
        if self._storage_method == Image.LINEAR_8BIT_RMO:
            return length
        if self._storage_method == Image.TILED_8BIT:
            return length * 64
        if self._storage_method == Image.PLANAR_4BIT:
            return length * 32
        if self._storage_method == Image.PLANAR_8BIT:
            return length * 64
        raise Exception(f'Image "{self.name}" was assigned an unknown storage method: {self._storage_method}')

    @staticmethod
    def get_linear_8bit(rom: "Rom", width: int, height: int):
        """Gets pixel data for an 8-bit image made from linear data (column major order)."""
        # noinspection PyUnusedLocal
        pixels = [[0 for x in range(width)] for y in range(height)]
        for x in range(width):
            for y in range(height):
                pixels[y][x] = rom.read_ubyte()
        return pixels

    @staticmethod
    def get_linear_8bit_rmo(rom: "Rom", width: int, height: int):
        """Gets pixel data for an 8-bit image made from linear data (row major order)."""
        # noinspection PyUnusedLocal
        pixels = [[0 for x in range(width)] for y in range(height)]
        for y in range(height):
            for x in range(width):
                pixels[y][x] = rom.read_ubyte()
        return pixels

    @staticmethod
    def get_tiled_8bit(rom: "Rom", tiles_wide: int, tiles_high: int):
        """Gets pixel data for an 8-bit image made from linear 8x8 tiles."""
        # noinspection PyUnusedLocal
        pixels = [[0 for x in range(tiles_wide * Image._TILE_SIZE)] for y in range(tiles_high * Image._TILE_SIZE)]
        for tile in range(tiles_wide * tiles_high):
            tile_x = (tile % tiles_wide) * Image._TILE_SIZE
            tile_y = (tile // tiles_wide) * Image._TILE_SIZE
            for y in range(Image._TILE_SIZE):
                for x in range(Image._TILE_SIZE):
                    pixels[tile_y + y][tile_x + x] = rom.read_ubyte()
        return pixels

    @staticmethod
    def get_planar_4bit(rom: "Rom", tiles_wide: int, tiles_high: int, start_color_index: int):
        """Gets pixel data for a 4-bit image made from planar 8x8 tiles.

        Note: Pixel data is returned as 8-bit pixels.
        """
        # noinspection PyUnusedLocal
        pixels = [[0 for x in range(tiles_wide * Image._TILE_SIZE)] for y in range(tiles_high * Image._TILE_SIZE)]
        for tile in range(tiles_wide * tiles_high):
            tile_x = (tile % tiles_wide) * Image._TILE_SIZE
            tile_y = (tile // tiles_wide) * Image._TILE_SIZE
            index = 0
            data = struct.unpack('32b', rom.read(32))
            for y in range(Image._TILE_SIZE):
                for x in range(Image._TILE_SIZE):
                    bit = 1 << (7 - x)
                    pixel = start_color_index
                    pixel |= 1 if (data[index] & bit) else 0
                    pixel |= 2 if (data[index + 1] & bit) else 0
                    pixel |= 4 if (data[index + 0x10] & bit) else 0
                    pixel |= 8 if (data[index + 0x11] & bit) else 0
                    pixels[tile_y + y][tile_x + x] = pixel
                index += 2
        return pixels

    @staticmethod
    def get_planar_8bit(rom: "Rom", tiles_wide: int, tiles_high: int):
        """Gets pixel data for an 8-bit image made from planar 8x8 tiles."""
        # TODO? Change the parameters to tile_count, tiles_wide so that non-rectangular groups of images can be loaded.
        #  This might be something to do for all tile-related methods.
        # noinspection PyUnusedLocal
        pixels = [[0 for x in range(tiles_wide * Image._TILE_SIZE)] for y in range(tiles_high * Image._TILE_SIZE)]
        for tile in range(tiles_wide * tiles_high):
            tile_x = (tile % tiles_wide) * Image._TILE_SIZE
            tile_y = (tile // tiles_wide) * Image._TILE_SIZE
            index = 0
            data = struct.unpack('64b', rom.read(64))
            for y in range(Image._TILE_SIZE):
                for x in range(Image._TILE_SIZE):
                    bit = 1 << (7 - x)
                    pixel = 0
                    pixel |= 1 if (data[index] & bit) else 0
                    pixel |= 2 if (data[index + 1] & bit) else 0
                    pixel |= 4 if (data[index + 0x10] & bit) else 0
                    pixel |= 8 if (data[index + 0x11] & bit) else 0
                    pixel |= 0x10 if (data[index + 0x20] & bit) else 0
                    pixel |= 0x20 if (data[index + 0x21] & bit) else 0
                    pixel |= 0x40 if (data[index + 0x30] & bit) else 0
                    pixel |= 0x80 if (data[index + 0x31] & bit) else 0
                    pixels[tile_y + y][tile_x + x] = pixel
                index += 2
        return pixels
