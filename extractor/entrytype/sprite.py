from image import Image
from ..utils import *

class Sprite(Image):
    _column_count = None
    # Constants
    SPRITE_SIZE = 64

    '''
    Constructor.
    Loads a sprite from the current file position.
    Index 255 is used to indicate transparency.
    '''
    def __init__(self, rom, name, column_count, palette):
        self._column_count = column_count
        Image.__init__(self, rom, name, None, Sprite.SPRITE_SIZE, Sprite.SPRITE_SIZE, palette, transparency_color_index=0xff)

    '''
    Gets the sprite pixels.
    Sprite data is converted into pixel data.
    '''
    def get_pixels(self, rom):
        pixels = [[self._transparency_color_index for x in range(self._width)] for y in range(self._height)]
        page_offset = (self.offset & 0xffff0000)
##        rom.seek(self.offset)
        pixel_x = (Sprite.SPRITE_SIZE - self._column_count) / 2
        for line in range(self._column_count):
            rom.seek(self.offset + line * 2)
            line_offset = page_offset + read_ushort(rom)
            while True:
                rom.seek(line_offset)
                line_offset += 6
                topY = read_ushort(rom)
                if topY == 0xffff:
                    break
                topY >>= 1
                bottomY = read_ushort(rom) / 2
                pixel_offset = read_ushort(rom)
                rom.seek(page_offset + pixel_offset + topY)
                for y in range(topY, bottomY):
                    pixels[y - 1][pixel_x] = read_ubyte(rom)
            pixel_x += 1
        return pixels

    '''
    Reads sprite offsets and column counts from the rom.
    Wolf3D-style, complex...
    '''
    @staticmethod
    def read_sprite_info_wolf3d(rom, column_count_offset, sprite_data_offset):
        rom.seek(column_count_offset)
        sprites = []
        while True:
            sprites.append({})
            sprite = sprites[-1]
            sprite['column_count'] = read_ubyte(rom)
            rom.read(1) # always 0
            offset = bytearray([0, 0, 0, 0])
            offset_index = read_ubyte(rom) - 1
            jump_amount = 0
            if offset_index < len(offset):
                while True:
                    byte = read_ubyte(rom)
                    if byte == 0:
                        break
                    offset[offset_index] = byte
                    offset_index += 1
                jump_amount = read_ubyte(rom)
            sprite['offset'] = sprite_data_offset + struct.unpack('<I', offset)[0]
            if jump_amount == 0x95: # Magic number for US!
                break
            if jump_amount == 0x91: # Magic number for beta 1!
                break
        return sprites

    '''
    Reads sprite offsets and column counts from the rom.
    SNA3D-style, simpler.
    '''
    @staticmethod
    def read_sprite_info_noah(rom, column_count_offset, sprite_data_offset):
        rom.seek(column_count_offset)
        sprites = []
        while True:
            line_count = read_ubyte(rom)
            if line_count == 0:
                break;
            sprites.append({})
            sprite = sprites[-1]
            sprite['column_count'] = line_count
            rom.read(1) # always 0
            sprite['offset'] = sprite_data_offset + struct.unpack('<I', rom.read(4))[0]
        return sprites
