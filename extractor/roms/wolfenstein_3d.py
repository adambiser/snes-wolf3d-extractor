import struct

from ..entrytype import *
from ..utils import insert_string


# These must be modified by rom info files using this one as their base.


def init(rom, **kwargs):
    # Using USA rom values as default.
    starting_offset = kwargs.get('starting_offset', 0x82ab3)
    has_ball_texture = kwargs.get('has_ball_texture', True)
    map_offset_list_offset = kwargs.get('map_offset_list_offset', 0xfc886)
    map_name_offset = kwargs.get('map_name_offset', 0x3958)
    sprite_info_offset = kwargs.get('sprite_info_offset', 0xfda6e)
    sound_info_offset_1 = kwargs.get('sound_info_offset_1', 0xe981e)
    sound_info_offset_2 = kwargs.get('sound_info_offset_2', 0xfc6b8)
    sound_group_2_count = kwargs.get('sound_group_2_count', 5)
    instrument_info_offset = kwargs.get('instrument_info_offset', 0x8b)
    song_offset_list_offset = kwargs.get('song_offset_list_offset', 0xfd7a1)
    is_japan = kwargs.get('is_japan', False)
    # If offset is -1, it is assumed to immediately follow the previous entry.
    rom.add_entry(InstrumentList(instrument_info_offset, 'instruments'))
    if has_ball_texture:
        rom.add_entry(Image(starting_offset, 'ball_texture', Image.LINEAR_8BIT_RMO, 64, 64, "main"))
        rom.add_entry(ByteData(-1, 1))  # There is 1 more byte, padding?
        rom.add_entry(Palette(-1, 'title'))
    else:
        rom.add_entry(Palette(starting_offset, 'title'))
    rom.add_entry(Palette(-1, 'title_dark'))
    rom.add_entry(ByteData(-1, 64))  # 64 bytes of unknown data.
    rom.add_entry(Image(-1, 'title_screen', Image.PLANAR_8BIT, 32, 25, "title"))
    rom.add_entry(Palette(-1, 'briefing'))
    if is_japan:
        rom.add_entry(Image(-1, 'mission_intro_1', Image.PLANAR_8BIT, 30, 4, "briefing"))
        rom.add_entry(Image(-1, 'mission_intro_2', Image.PLANAR_8BIT, 20, 4, "briefing"))
        rom.add_entry(Image(-1, 'mission_intro_3', Image.PLANAR_8BIT, 30, 4, "briefing"))
        rom.add_entry(Image(-1, 'mission_intro_4', Image.PLANAR_8BIT, 27, 4, "briefing"))
        rom.add_entry(Image(-1, 'mission_intro_5', Image.PLANAR_8BIT, 13, 4, "briefing"))
        rom.add_entry(Image(-1, 'mission_intro_6', Image.PLANAR_8BIT, 23, 4, "briefing"))
    else:
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
    rom.add_entry(Image(-1, 'intermission_number_0', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_number_1', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_number_2', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_number_3', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_number_4', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_number_5', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_number_6', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_number_7', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_number_8', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_number_9', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_percent', Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'intermission_exclamation', Image.PLANAR_4BIT, 1, 2, "intermission", 0x20, 0x20))
    rom.add_entry(Image(-1, 'overhead_map_tiles', Image.PLANAR_8BIT, 8, 5, "main"))
    rom.add_entry(Palette(-1, 'main'))
    rom.add_entry(ByteData(-1, 0x2300))  # Unknown data that's 0x2300 bytes long.
    rom.add_entry(Image(-1, 'status_bar_left_text', Image.PLANAR_4BIT, 14, 1, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'status_bar_percent', Image.PLANAR_4BIT, 1, 2, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'status_bar_right_text', Image.PLANAR_4BIT, 11, 1, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'status_bar', Image.TILED_8BIT, 14, 2, "main"))
    rom.add_entry(Image(-1, 'font', Image.PLANAR_4BIT, 16, 6, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'status_bar_numbers', Image.PLANAR_4BIT, 16, 2, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'status_bar_faces', Image.PLANAR_4BIT, 16, 8, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'weapon_0', Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'weapon_1', Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'weapon_2', Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'weapon_3', Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'weapon_4', Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0))
    rom.add_entry(Image(-1, 'weapon_5', Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0))
    # Add maps
    # Map offsets are stored as: 00 01 35 03 CC
    # final CC needs to be converted to be 0C
    # 00 01 appears to mark index entries.
    map_offsets = read_rom_address_list(rom, map_offset_list_offset, 30)
    for x in range(len(map_offsets)):
        entry_name = rom.read_text_chunk(map_name_offset + x * 3, 2)
        entry_name = 'Map ' + insert_string(entry_name, 1, '-')
        rom.add_entry(Map(map_offsets[x], entry_name))
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
    sprite_info = read_sprite_info(rom, sprite_info_offset, 0x30000)
    for x in range(len(sprite_info)):
        entry_name = 'sprite_{:03d}'.format(x)
        rom.add_entry(
            Sprite(sprite_info[x]['offset'],
                   entry_name,
                   sprite_info[x]['column_count'], "main"
                   )
            )
    # Sounds
    sound_info = Sound.read_sound_info(rom, sound_info_offset_1, sound_info_offset_2, sound_group_2_count)
    for x in range(len(sound_info)):
        entry_name = 'sound_{:02d}'.format(x)
        rom.add_entry(
            Sound(sound_info[x]['offset'],
                  entry_name,
                  sound_info[x]['loop_offset']
                  )
            )
    # Songs
    song_offsets = read_rom_address_list(rom, song_offset_list_offset, 12)
    for x in range(len(song_offsets)):
        entry_name = 'song_{:02d}'.format(x)
        rom.add_entry(Song(song_offsets[x], entry_name))


def read_rom_address_list(rom, offset, count):
    """Reads a list of addresses in Wolf3D's weird storage method.
    01 35 03 CC 00 -> 0xc0335
    """
    rom.seek(offset)
    offsets = []
    for x in range(count):
        zb = rom.read_ubyte()
        assert 1 <= zb <= 3, 'zb is {}'.format(zb)
        zb -= 1
        address = b'\00' * zb + rom.read(4 - zb)
        offsets.append(struct.unpack('<I', address)[0] - 0xc00000)
    return offsets


def read_sprite_info(rom, column_count_offset, sprite_data_offset):
    """Reads sprite offsets and column counts from the rom.

    Wolf3D-style, complex...
    """
    rom.seek(column_count_offset)
    sprites = []
    while True:
        sprite_info = {
            'column_count': rom.read_ushort(),
        }
        offset = bytearray([0, 0, 0, 0])
        offset_index = rom.read_ubyte() - 1
        jump_amount = 0
        if offset_index < len(offset):
            while True:
                byte = rom.read_ubyte()
                if byte == 0:
                    break
                offset[offset_index] = byte
                offset_index += 1
            jump_amount = rom.read_ubyte()
        sprite_info['offset'] = sprite_data_offset + struct.unpack('<I', offset)[0]
        sprites.append(sprite_info)
        # Test if this bit is set and if so, stop.
        # Probably not the way it worked, but it works for all roms.
        if jump_amount & 0x80:
            break
    return sprites
