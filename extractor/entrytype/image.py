'''
Requires PyPNG which can be found at https://github.com/drj11/pypng
The only file needed is /code/png.py. Place it in the same folder as this file.
'''
from entry import Entry
from ..utils import *
from ..png import png

class Image(Entry):
    _pixels = None
    _palette = None
    _width = None
    _height = None
    _storage_method = None
    _start_color_index = None
    _transparency_color_index = None
    # Image storage method constants.
    LINEAR_8BIT = 1
    LINEAR_8BIT_RMO = 2 # Row Major Order
    TILED_8BIT = 3
    PLANAR_4BIT = 4
    PLANAR_8BIT = 5

    '''
    Constructor.
    Loads an image from the current file position using the given storage method.
    '''
    def __init__(self, rom, name, storage_method, width, height, palette, start_color_index=None, transparency_color_index=None):
        Entry.__init__(self, rom, name)
        self._storage_method = storage_method
        self._width = width
        self._height = height
        self._palette = rom.get_entry(palette)
        rom.seek(self.offset)
        self._transparency_color_index = transparency_color_index
        self._start_color_index = start_color_index
        self._pixels = self.get_pixels(rom)

    '''
    Gets the pixel data for the image.
    '''
    def get_pixels(self, rom):
        if self._storage_method == Image.LINEAR_8BIT:
            return Image.get_linear_8bit(rom, self._width, self._height)
        elif self._storage_method == Image.LINEAR_8BIT_RMO:
            return Image.get_linear_8bit_rmo(rom, self._width, self._height)
        elif self._storage_method == Image.TILED_8BIT:
            return Image.get_tiled_8bit(rom, self._width, self._height)
        elif self._storage_method == Image.PLANAR_4BIT:
            return Image.get_planar_4bit(rom, self._width, self._height, self._start_color_index)
        elif self._storage_method == Image.PLANAR_8BIT:
            return Image.get_planar_8bit(rom, self._width, self._height)
        else:
            raise Exception('Unknown image storage method value: ' + str(self._storage_method))
        

    '''
    Gets the data length of an image.
    This is the length of data read from the rom, not the returned pixel data length.
    '''
    @staticmethod
    def get_data_length(storage_method, width, height, *ignored):
        length = width * height
        if storage_method == Image.LINEAR_8BIT:
            return length
        if storage_method == Image.LINEAR_8BIT_RMO:
            return length
        if storage_method == Image.TILED_8BIT:
            return length * 64
        if storage_method == Image.PLANAR_4BIT:
            return length * 32
        if storage_method == Image.PLANAR_8BIT:
            return length * 64
        raise Exception('Could not determine data length for function: ' + str(storage_method))

    '''
    Gets pixel data for an 8-bit image made from linear data (column major order).
    '''
    @staticmethod
    def get_linear_8bit(f, width, height):
        pixels = [[0 for x in range(width)] for y in range(height)]
        for x in range(width):
            for y in range(height):
                pixels[y][x] = read_ubyte(f)
        return pixels

    '''
    Gets pixel data for an 8-bit image made from linear data (row major order).
    '''
    @staticmethod
    def get_linear_8bit_rmo(rom, width, height):
        pixels = [[0 for x in range(width)] for y in range(height)]
        for y in range(height):
            for x in range(width):
                pixels[y][x] = read_ubyte(rom)
        return pixels

    '''
    Gets pixel data for an 8-bit image made from linear 8x8 tiles.
    '''
    @staticmethod
    def get_tiled_8bit(rom, tiles_wide, tiles_high):
        tile_size = 8
        pixels = [[0 for x in range(tiles_wide * tile_size)] for y in range(tiles_high * tile_size)]
        for tile in range(tiles_wide * tiles_high):
            tile_x = (tile % tiles_wide) * tile_size
            tile_y = (tile / tiles_wide) * tile_size
            for y in range(tile_size):
                for x in range(tile_size):
                    pixels[tile_y + y][tile_x + x] = read_ubyte(rom)
        return pixels

    '''
    Gets pixel data for a 4-bit image made from planar 8x8 tiles.
    Note: Pixel data is returned as 8-bit pixels.
    '''
    @staticmethod
    def get_planar_4bit(rom, tiles_wide, tiles_high, start_color_index):
        tile_size = 8
        pixels = [[0 for x in range(tiles_wide * tile_size)] for y in range(tiles_high * tile_size)]
        for tile in range(tiles_wide * tiles_high):
            tile_x = (tile % tiles_wide) * tile_size
            tile_y = (tile / tiles_wide) * tile_size
            index = 0
            data = struct.unpack('32b', rom.read(32))
            for y in range(tile_size):
                for x in range(tile_size):
                    bit = 1 << (7 - x)
                    pixel = start_color_index
                    pixel |= 1 if (data[index] & bit) else 0
                    pixel |= 2 if (data[index + 1] & bit) else 0
                    pixel |= 4 if (data[index + 0x10] & bit) else 0
                    pixel |= 8 if (data[index + 0x11] & bit) else 0
                    pixels[tile_y + y][tile_x + x] = pixel
                index += 2
        return pixels

    '''
    Gets pixel data for an 8-bit image made from planar 8x8 tiles.
    '''
    @staticmethod
    def get_planar_8bit(rom, tiles_wide, tiles_high):
        tile_size = 8
        pixels = [[0 for x in range(tiles_wide * tile_size)] for y in range(tiles_high * tile_size)]
        for tile in range(tiles_wide * tiles_high):
            tile_x = (tile % tiles_wide) * tile_size
            tile_y = (tile / tiles_wide) * tile_size
            index = 0
            data = struct.unpack('64b', rom.read(64))
            for y in range(tile_size):
                for x in range(tile_size):
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

    '''
    Saves the given pixel data to the given filename.
    This always saves the image using a bitdepth of 8, even if the image is stored in the rom as 4-bit.
    '''
    def save(self, filename):
        # Clone the given palette so a color index can become transparent without affecting it.
        temp_palette = self._palette.colors[:]
        if not self._transparency_color_index is None:
            temp_palette[self._transparency_color_index] = (0xff, 0xff, 0xff, 0)
        with open(filename, 'wb') as f:
            w = png.Writer(len(self._pixels[0]), len(self._pixels), palette=temp_palette, bitdepth=8)
            w.write(f, self._pixels)

    '''
    Returns the default file extension to use while saving.
    Should begin with a period.
    '''
    def get_default_extension(self):
        return ".png"
