from entrytype import *
import binascii
import struct
import utils
from importlib import import_module
from utils import *

'''
Help for finding entries:
First Map:
- Search for "TELAS"
- Go forward 0x38 bytes. This should be the offset of the first map.
- Search for the hex values of this offset + 0xc00000.
'''

'''
TODO
Add map names
For both Wolf and Noah:
11 12 1B 21 22 23 2B 31 32 33 3B 3S 41 42 43 44 4B 51 52 53 54 55 5B 61 62 63 64 65 6B 6S

Allow for non-retangular tiled image extraction
Example from S3DNA:
    [-1, 'overhead_map_tiles_1', Image, Image.PLANAR_8BIT, 8, 5, "main"],
    [-1, 'overhead_map_tiles_2', Image, Image.PLANAR_8BIT, 7, 1, "main"],
'''

class Rom:
    crc32 = None
    filename = None
    rom_name = None
    _entry_cache = {}
    '''
    Constructor.
    The crc32 of the given file is used to determine which information to use for the extraction.
    '''
    def __init__(self, filename):
##        # Set up supported ROM information.
##        rom_list = {
##                'a2315a14' : {
##                    'name' : "Super Noah's Ark 3D (1994)",
##                    'entries' : [
##                        # offset, name, class, constructor arguments...
##                        # If offset is -1, it is assumed to immediately follow the previous entry.
##                        [0x76168, 'title', Palette],
##                        [-1, 'title_dark', Palette],
##                        [-1, 'unknown', ByteData, 64], # 64 bytes of unknown data.
##                        [-1, 'title_screen', Image, Image.PLANAR_8BIT, 32, 25, "title"],
##                        [-1, 'briefing', Palette],
##                        [-1, 'unknown', ByteData, 64], # 64 bytes of unknown data.
##                        [-1, 'mission_briefing', Image, Image.PLANAR_8BIT, 32, 24, "briefing"],
##                        [-1, 'intermission', Palette],
##                        [-1, 'intermission_background', Image, Image.PLANAR_4BIT, 8, 8, "intermission", 0x50],
##                        [-1, 'intermission_player', Image, Image.PLANAR_4BIT, 11, 33, "intermission", 0x00],
##                        [-1, 'intermission_mission', Image, Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_floor', Image, Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_complete', Image, Image.PLANAR_4BIT, 17, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_time', Image, Image.PLANAR_4BIT, 9, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_enemy', Image, Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_par', Image, Image.PLANAR_4BIT, 8, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_treasure', Image, Image.PLANAR_4BIT, 17, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_score', Image, Image.PLANAR_4BIT, 11, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_secret', Image, Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_bonus', Image, Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_perfect', Image, Image.PLANAR_4BIT, 15, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_speed', Image, Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_of', Image, Image.PLANAR_4BIT, 4, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_overall', Image, Image.PLANAR_4BIT, 15, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_colon', Image, Image.PLANAR_4BIT, 1, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_0', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_1', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_2', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_3', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_4', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_5', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_6', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_7', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_8', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_9', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_percent', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_exclamation', Image, Image.PLANAR_4BIT, 1, 2, "intermission", 0x20, 0x20],
##                        # NOTE: This is different from the Wolf3D rom.
##                        [-1, 'overhead_map_tiles_1', Image, Image.PLANAR_8BIT, 8, 5, "main"],
##                        [-1, 'overhead_map_tiles_2', Image, Image.PLANAR_8BIT, 7, 1, "main"],
##                        [-1, 'main', Palette],
##                        [-1, 'unknown', ByteData, 0x2300], # Unknown data that's 0x2300 bytes long.
##                        [-1, 'status_bar_left_text', Image, Image.PLANAR_4BIT, 14, 1, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar_percent', Image, Image.PLANAR_4BIT, 1, 2, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar_right_text', Image, Image.PLANAR_4BIT, 11, 1, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar', Image, Image.TILED_8BIT, 14, 2, "main"],
##                        [-1, 'font', Image, Image.PLANAR_4BIT, 16, 6, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar_numbers', Image, Image.PLANAR_4BIT, 16, 2, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar_faces', Image, Image.PLANAR_4BIT, 16, 8, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_0', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_1', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_2', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_3', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_4', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_5', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        ],
##                    'entry_lists': [
##                        # class, count, offset lambda, naming lambda
##                        # Map offsets are stored as: 4A C9 CA 00
##                        # CA needs to become 0A.
##                        [ Map,
##                          30,
##                          lambda x: self._read_address(0xfc820 + x * 4),
##                          lambda x: 'Map ' + utils.insert_string(self._read_text(0xfca65 + x * 3, 2), 1, '-')],
##                        [ Image,
##                          64,
##                          lambda x: 0x20000 + x * 32 * 32,
##                          lambda x: 'wall_' + str(x),
##                          Image.LINEAR_8BIT, 32, 32, "main"],
##                        [ Sprite,
##                          lambda: self._store_and_get_length(self._sprites, Sprite.read_sprite_info_noah(self, 0xfdd6f, 0x30000)),
##                          lambda x: self._sprites[x]['offset'],
##                          lambda x: 'sprite_' + str(x),
##                          lambda x: self._sprites[x]['column_count'],
##                          "main"],
##                        [ Sound,
##                          lambda: self._store_and_get_length(self._sounds, Sound.read_sound_info(self, 0xdd791, 0xfc70a, 19)),
##                          lambda x: self._sounds[x]['offset'],
##                          lambda x: 'sound_' + str(x),
##                          lambda x: self._sounds[x]['loop_offset']],
##                        ],
##                },
##                '6582a8f5' : {
##                    'name' : "Wolfenstein 3D (USA)",
##                    'entries' : [
##                        # offset, name, class, constructor arguments...
##                        # If offset is -1, it is assumed to immediately follow the previous entry.
##                        [0x82ab3, 'ball_texture', Image, Image.LINEAR_8BIT_RMO, 64, 64, "main"],
##                        [-1, 'unknown', ByteData, 1], # There is 1 more byte, padding?
##                        [-1, 'title', Palette],
##                        [-1, 'title_dark', Palette],
##                        [-1, 'unknown', ByteData, 64], # 64 bytes of unknown data.
##                        [-1, 'title_screen', Image, Image.PLANAR_8BIT, 32, 25, "title"],
##                        [-1, 'briefing', Palette],
##                        [-1, 'unknown', ByteData, 64], # 64 bytes of unknown data.
##                        [-1, 'mission_briefing', Image, Image.PLANAR_8BIT, 32, 24, "briefing"],
##                        [-1, 'intermission', Palette],
##                        [-1, 'intermission_background', Image, Image.PLANAR_4BIT, 8, 8, "intermission", 0x50],
##                        [-1, 'intermission_player', Image, Image.PLANAR_4BIT, 11, 33, "intermission", 0x00],
##                        [-1, 'intermission_mission', Image, Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_floor', Image, Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_complete', Image, Image.PLANAR_4BIT, 17, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_time', Image, Image.PLANAR_4BIT, 9, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_enemy', Image, Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_par', Image, Image.PLANAR_4BIT, 8, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_treasure', Image, Image.PLANAR_4BIT, 17, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_score', Image, Image.PLANAR_4BIT, 11, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_secret', Image, Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_bonus', Image, Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_perfect', Image, Image.PLANAR_4BIT, 15, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_speed', Image, Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_of', Image, Image.PLANAR_4BIT, 4, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_overall', Image, Image.PLANAR_4BIT, 15, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_colon', Image, Image.PLANAR_4BIT, 1, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_0', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_1', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_2', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_3', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_4', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_5', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_6', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_7', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_8', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_9', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_percent', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_exclamation', Image, Image.PLANAR_4BIT, 1, 2, "intermission", 0x20, 0x20],
##                        [-1, 'overhead_map_tiles', Image, Image.PLANAR_8BIT, 8, 5, "main"],
##                        [-1, 'main', Palette],
##                        [-1, 'unknown', ByteData, 0x2300], # Unknown data that's 0x2300 bytes long.
##                        [-1, 'status_bar_left_text', Image, Image.PLANAR_4BIT, 14, 1, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar_percent', Image, Image.PLANAR_4BIT, 1, 2, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar_right_text', Image, Image.PLANAR_4BIT, 11, 1, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar', Image, Image.TILED_8BIT, 14, 2, "main"],
##                        [-1, 'font', Image, Image.PLANAR_4BIT, 16, 6, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar_numbers', Image, Image.PLANAR_4BIT, 16, 2, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar_faces', Image, Image.PLANAR_4BIT, 16, 8, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_0', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_1', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_2', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_3', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_4', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_5', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        ],
##                    'entry_lists': [
##                        # class, count, offset lambda, naming lambda
##                        # Map offsets are stored as: 00 01 35 03 CC
##                        # final CC needs to be converted to be 0C
##                        # 00 01 appears to mark index entries.
##                        [ Map,
##                          lambda: self._store_and_get_length(self._map_offsets, self._read_rom_address_list_wolf(0xfc886, 30)),
##                          lambda x: self._map_offsets[x],
##                          lambda x: 'Map ' + utils.insert_string(self._read_text(0x3958 + x * 3, 2), 1, '-')],
##                        [ Image,
##                          64,
##                          lambda x: 0x20000 + x * 32 * 32,
##                          lambda x: 'wall_' + str(x),
##                          Image.LINEAR_8BIT, 32, 32, "main"],
##                        [ Sprite,
##                          lambda: self._store_and_get_length(self._sprites, Sprite.read_sprite_info_wolf3d(self, 0xfda6e, 0x30000)),
##                          lambda x: self._sprites[x]['offset'],
##                          lambda x: 'sprite_' + str(x),
##                          lambda x: self._sprites[x]['column_count'],
##                          "main"],
##                        [ Sound,
##                          lambda: self._store_and_get_length(self._sounds, Sound.read_sound_info(self, 0xe981e, 0xfc6b8, 5)),
##                          lambda x: self._sounds[x]['offset'],
##                          lambda x: 'sound_' + str(x),
##                          lambda x: self._sounds[x]['loop_offset']],
##                        ],
##                },
##                # 63e442b4 - beta 1
##                '63e442b4' : {
##                    'name' : "Wolfenstein 3D (Beta 1)",
##                    'entries' : [
##                        # offset, name, class, constructor arguments...
##                        # If offset is -1, it is assumed to immediately follow the previous entry.
####                        [0x82ab3, 'ball_texture', Image, Image.LINEAR_8BIT_RMO, 64, 64, "main"],
####                        [-1, 'unknown', ByteData, 1], # There is 1 more byte, padding?
##                        [0x87280, 'title', Palette],
##                        [-1, 'title_dark', Palette],
##                        [-1, 'unknown', ByteData, 64], # 64 bytes of unknown data.
##                        [-1, 'title_screen', Image, Image.PLANAR_8BIT, 32, 25, "title"],
##                        [-1, 'briefing', Palette],
##                        [-1, 'unknown', ByteData, 64], # 64 bytes of unknown data.
##                        [-1, 'mission_briefing', Image, Image.PLANAR_8BIT, 32, 24, "briefing"],
##                        [-1, 'intermission', Palette],
##                        [-1, 'intermission_background', Image, Image.PLANAR_4BIT, 8, 8, "intermission", 0x50],
##                        [-1, 'intermission_player', Image, Image.PLANAR_4BIT, 11, 33, "intermission", 0x00],
##                        [-1, 'intermission_mission', Image, Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_floor', Image, Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_complete', Image, Image.PLANAR_4BIT, 17, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_time', Image, Image.PLANAR_4BIT, 9, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_enemy', Image, Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_par', Image, Image.PLANAR_4BIT, 8, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_treasure', Image, Image.PLANAR_4BIT, 17, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_score', Image, Image.PLANAR_4BIT, 11, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_secret', Image, Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_bonus', Image, Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_perfect', Image, Image.PLANAR_4BIT, 15, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_speed', Image, Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_of', Image, Image.PLANAR_4BIT, 4, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_overall', Image, Image.PLANAR_4BIT, 15, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_colon', Image, Image.PLANAR_4BIT, 1, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_0', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_1', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_2', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_3', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_4', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_5', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_6', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_7', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_8', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_number_9', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_percent', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
##                        [-1, 'intermission_exclamation', Image, Image.PLANAR_4BIT, 1, 2, "intermission", 0x20, 0x20],
##                        [-1, 'overhead_map_tiles', Image, Image.PLANAR_8BIT, 8, 5, "main"],
##                        [-1, 'main', Palette],
##                        [-1, 'unknown', ByteData, 0x2300], # Unknown data that's 0x2300 bytes long.
##                        [-1, 'status_bar_left_text', Image, Image.PLANAR_4BIT, 14, 1, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar_percent', Image, Image.PLANAR_4BIT, 1, 2, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar_right_text', Image, Image.PLANAR_4BIT, 11, 1, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar', Image, Image.TILED_8BIT, 14, 2, "main"],
##                        [-1, 'font', Image, Image.PLANAR_4BIT, 16, 6, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar_numbers', Image, Image.PLANAR_4BIT, 16, 2, "main", 0xf0, 0xf0],
##                        [-1, 'status_bar_faces', Image, Image.PLANAR_4BIT, 16, 8, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_0', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_1', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_2', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_3', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_4', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        [-1, 'weapon_5', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
##                        ],
##                    'entry_lists': [
##                        # class, count, offset lambda, naming lambda
##                        # Map offsets are stored as: 00 01 35 03 CC
##                        # final CC needs to be converted to be 0C
##                        # 00 01 appears to mark index entries.
##                        [ Map,
##                          lambda: self._store_and_get_length(self._map_offsets, self._read_rom_address_list_wolf(0xfb886, 30)),
##                          lambda x: self._map_offsets[x],
##                          lambda x: 'Map ' + self._read_text(0x3268 + x * 3, 2)],
##                        [ Image,
##                          64,
##                          lambda x: 0x20000 + x * 32 * 32,
##                          lambda x: 'wall_' + str(x),
##                          Image.LINEAR_8BIT, 32, 32, "main"],
##                        [ Sprite,
##                          lambda: self._store_and_get_length(self._sprites, Sprite.read_sprite_info_wolf3d(self, 0xfca47, 0x30000)),
##                          lambda x: self._sprites[x]['offset'],
##                          lambda x: 'sprite_' + str(x),
##                          lambda x: self._sprites[x]['column_count'],
##                          "main"],
##                        [ Sound,
##                          lambda: self._store_and_get_length(self._sounds, Sound.read_sound_info(self, 0xec44b, 0xfb6b8, 5)),
##                          lambda x: self._sounds[x]['offset'],
##                          lambda x: 'sound_' + str(x),
##                          lambda x: self._sounds[x]['loop_offset']],
##                        ],
##                },
##                # 2bebdb00 - beta 2
##                # 9c3869d0 - usa, but starts at 0x200 bytes
##                # 6a455ee2 - europe
##                # cc47b8f9 - japan
##            }
##        # The 2013 Steam release of SNA3D is the same as 1994 version but with a newer copyright.
##        rom_list['643d5097'] = rom_list['a2315a14'].copy()
##        rom_list['643d5097']['name'] = "Super Noah's Ark 3D (2013)"
        # Now detect what rom was given.
        self.filename = filename
        self.crc32 = format(self.get_crc32(), '8x')
        self.info = import_module('.' + self.crc32, 'extractor.roms')
        self.info = getattr(self.info, 'RomInfo')(self)
##        from self.info import rom_info
##        self.info = getattr(self.info.roms, self.crc32)
##        print [name for name in dir(self.info) if not name.startswith('_')]
##        self.info = rom_list.get(self.crc32)
        if self.info is None:
            raise Exception('Did not find ROM information for crc32: ' + self.crc32)
        print 'Detected ROM: %s (crc32: %s)' % (self.info.name, self.crc32)
        self.rom_name = self.info.name
        # Find/Load data offsets
        # Fill in any image offsets that are blank.
        for index in range(1, self.get_entry_count()):
            entry = self.info.entries[index]
            if entry[0] == -1:
                prev_entry = self.info.entries[index - 1]
                entry[0] = prev_entry[0] + prev_entry[2].get_data_length(*prev_entry[3:])
        # Load entry lists into the main entry list.
        with self:
            for lst in self.info.entry_lists:
                if callable(lst[1]):
                    entry_count = lst[1](self.info)
                else:
                    entry_count = lst[1]
                for x in range(entry_count):
                    temp = lst[:] # clone list
                    # call everything that's callable for this iteration.
                    for index in range(2, len(temp)):
                        if callable(temp[index]):
                            temp[index] = temp[index](self.info, x)
                    self.info.entries.append([temp[2], temp[3], temp[0]] + temp[4:])

    '''
    Opens the rom for reading.
    '''
    def __enter__(self):
        self.open()
        return self

    '''
    Closes the inner rom file object.
    '''
    def __exit__(self, *a):
        self.close()
        return False

    '''
    Calculates the unsigned crc32 value for the rom.
    '''
    def get_crc32(self):
        with self:
            buf = self.read()
        return (binascii.crc32(buf) & 0xFFFFFFFF)

    '''
    Opens the rom for reading.
    '''
    def open(self):
        self.f = open(self.filename, 'rb')

    '''
    Closes the inner rom file object.
    '''
    def close(self):
        self.f.close()

    '''
    Reads the given number of bytes from the rom.
    '''
    def read(self, size=-1):
        return self.f.read(size)

    '''
    Move to a new file position.
    '''
    def seek(self, offset, whence=0):
        self.f.seek(offset, whence)

    '''
    Returns the current file position.
    '''
    def tell(self):
        return self.f.tell()

    '''
    Returns the number of entries in the rom.
    '''
    def get_entry_count(self):
        return len(self.info.entries)

    '''
    Reads three bytes from the current location within the rom and converts it to an offset.
    '''
    def read_rom_address(self):
        return (struct.unpack('<i', self.read(3) + '\x00')[0] - 0xc00000) & 0xffffff

    '''
    Gets the index of an entry by name.
    '''
    def get_entry_index(self, name):
        return [entry[1] for entry in self.info.entries].index(name)

    '''
    Gets an entry from the rom.
    '''
    def get_entry_type(self, index):
        if isinstance(index, basestring):
            index = self.get_entry_index(index)
        return self.info.entries[index][2]

    '''
    Gets a list of indices of entries with the given class
    '''
    def get_entries_of_class(self, cls):
        return [x for x in range(len(self.info.entries)) if self.info.entries[x][2] is cls]

    '''
    Gets an entry from the rom.
    '''
    def get_entry(self, index):
        if isinstance(index, basestring):
            index = self.get_entry_index(index)
        # Check the entry cache for an existing value and return it if found.
        entry = self._entry_cache.get(index)
        if not entry is None:
            return entry
        info = self.info.entries[index]
        self.seek(info[0])
        entry = info[2](self, info[1], *info[3:])
        # Cache palettes for faster loading.
        if isinstance(entry, Palette):
            self._entry_cache[index] = entry
        return entry

    '''
    Gets text from an offset within the rom.
    '''
    def read_text_chunk(self, offset, length):
        self.seek(offset)
        return self.read(length)

    '''
    Reads a rom address from an offset within the rom.
    '''
    def _read_address(self, lookup_offset):
        self.seek(lookup_offset)
        return self.read_rom_address()

    '''
    Prints the list of entries (offset and name) sorted by offset.
    '''
    def print_entry_list(self):
        entries = sorted(i[0:2] for i in self.info.entries)
        for e in entries:
            print '0x{:x} - {}'.format(e[0], e[1])

    '''
    Reads a list of addresses in Wolf3D's weird storage method.
    '''
    def read_rom_address_list_wolf(self, offset, count):
        self.seek(offset)
        offsets = []
        for x in range(count):
            zb = read_ubyte(self)
            assert 1 <= zb <= 3
            zb -= 1
            address = '\00' * zb + self.read(4 - zb)
            offsets.append(struct.unpack('<I', address)[0] - 0xc00000)
        return offsets
