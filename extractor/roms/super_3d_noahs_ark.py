from ..entrytype import *
from ..utils import insert_string
import struct

'''
TODO
Allow for non-rectangular tiled image extraction
Example from S3DNA:
    [-1, 'overhead_map_tiles_1', Image, Image.PLANAR_8BIT, 8, 5, "main"],
    [-1, 'overhead_map_tiles_2', Image, Image.PLANAR_8BIT, 7, 1, "main"],
'''


def init(rom, **kwargs):
    instrument_info_offset = kwargs.get('instrument_info_offset', 0x130)
    starting_offset = kwargs.get('starting_offset', 0x76168)
    # If offset is -1, it is assumed to immediately follow the previous entry.
    rom.add_entry(InstrumentList(instrument_info_offset, 'instruments'))
    rom.add_entry(Palette(starting_offset, 'title'))
    rom.add_entry(Palette(-1, 'title_dark'))
    rom.add_entry(ByteData(-1, 64))  # 64 bytes of unknown data.
    rom.add_entry(Image(-1, 'title_screen', Image.PLANAR_8BIT, 32, 25, "title"))
    rom.add_entry(Palette(-1, 'briefing'))
    rom.add_entry(ByteData(-1, 64))  # 64 bytes of unknown data.
    rom.add_entry(Image(-1, 'mission_briefing', Image.PLANAR_8BIT, 32, 24, "briefing"))
    rom.add_entry(Palette(-1, 'intermission'))
    rom.add_entry(Image(-1, 'intermission_background', Image.PLANAR_4BIT, 8, 8, "intermission", 0x50))
    rom.add_entry(Image(-1, 'intermission_player', Image.PLANAR_4BIT, 11, 33, "intermission", 0x00))
    rom.add_entry(Image(-1, 'intermission_mission', Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_floor', Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_complete', Image.PLANAR_4BIT, 17, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_time', Image.PLANAR_4BIT, 9, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_enemy', Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_par', Image.PLANAR_4BIT, 8, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_treasure', Image.PLANAR_4BIT, 17, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_score', Image.PLANAR_4BIT, 11, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_secret', Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_bonus', Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_perfect', Image.PLANAR_4BIT, 15, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_speed', Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_of', Image.PLANAR_4BIT, 4, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_overall', Image.PLANAR_4BIT, 15, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_colon', Image.PLANAR_4BIT, 1, 2, "intermission", 0x20, 0x20))
    for x in range(10):
        rom.add_entry(Image(-1, f'intermission_number_{x}', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_percent', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_exclamation', Image.PLANAR_4BIT, 1, 2, "intermission", 0x20, 0x20))
    # NOTE: This is different from the Wolf3D rom.
    rom.add_entry(Image(-1, 'overhead_map_tiles_1', Image.PLANAR_8BIT, 8, 5, "main"))
    rom.add_entry(Image(-1, 'overhead_map_tiles_2', Image.PLANAR_8BIT, 7, 1, "main"))
    rom.add_entry(Palette(-1, 'main'))
    rom.add_entry(ByteData(-1, 0x2300)) # Unknown data that's 0x2300 bytes long.
    rom.add_entry(Image(-1, 'status_bar_left_text', Image.PLANAR_4BIT, 14, 1, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'status_bar_percent', Image.PLANAR_4BIT, 1, 2, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'status_bar_right_text', Image.PLANAR_4BIT, 11, 1, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'status_bar', Image.TILED_8BIT, 14, 2, "main"))
    rom.add_entry(Image(-1, 'font', Image.PLANAR_4BIT, 16, 6, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'status_bar_numbers', Image.PLANAR_4BIT, 16, 2, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'status_bar_faces', Image.PLANAR_4BIT, 16, 8, "main", 0xf0, 0xf0))
    for x in range(6):
        rom.add_entry(Image(-1, f'weapon_{x}', Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0))
    # Add maps
    # Map offsets are stored as: 4A C9 CA 00
    # CA needs to become 0A.
    for x in range(31):
        map_offset = rom.read_rom_address_from(0xfc820 + x * 4)
        if x < 30:
            entry_name = rom.read_text_chunk(0xfca65 + x * 3, 2)
            entry_name = 'Map ' + insert_string(entry_name, 1, '-')
        else:
            entry_name = 'Game Over'
        rom.add_entry(Map(map_offset, entry_name))
    # Add walls
    for x in range(64):
        entry_name = 'wall_{:02d}'.format(x)
        rom.add_entry(
            Image(0x20000 + x * 32 * 32,
                  entry_name,
                  Image.LINEAR_8BIT, 32, 32, "main"
                  )
            )
    # Add sprites
    sprite_info = read_sprite_info_(rom, 0xfdd6f, 0x30000)
    for x in range(len(sprite_info)):
        entry_name = 'sprite_{:03d}'.format(x)
        rom.add_entry(
            Sprite(sprite_info[x]['offset'],
                   entry_name,
                   sprite_info[x]['column_count'], "main"
                   )
            )
    # Add sounds
    sound_info = Sound.read_sound_info(rom, 0xdd791, 0xfc70a, 19)
    for x in range(len(sound_info)):
        entry_name = 'sound_{:02d}'.format(x)
        rom.add_entry(
            Sound(sound_info[x]['offset'],
                  entry_name,
                  sound_info[x]['loop_offset']
                  )
            )
    # Songs
    for x in range(11):
        entry_name = 'song_{:02d}'.format(x)
        entry_offset = rom.read_rom_address_from(0xFD881 + x * 4)
        rom.add_entry(Song(entry_offset, entry_name))


def read_sprite_info_(rom, column_count_offset, sprite_data_offset):
    """
    Reads sprite offsets and column counts from the rom.

    SNA3D-style, simpler.
    """
    rom.seek(column_count_offset)
    sprites = []
    while True:
        line_count = rom.read_ushort()
        if line_count == 0:
            break
        sprites.append({
            'column_count': line_count,
            'offset': sprite_data_offset + struct.unpack('<I', rom.read(4))[0],
        })
    return sprites
