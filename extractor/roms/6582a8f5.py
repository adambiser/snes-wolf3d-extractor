from ..entrytype import *
import extractor.utils as utils

class RomInfo:
    name = "Wolfenstein 3D (USA)"
    entries = [
        # offset, name, class, constructor arguments...
        # If offset is -1, it is assumed to immediately follow the previous entry.
        [0x82ab3, 'ball_texture', Image, Image.LINEAR_8BIT_RMO, 64, 64, "main"],
        [-1, 'unknown', ByteData, 1], # There is 1 more byte, padding?
        [-1, 'title', Palette],
        [-1, 'title_dark', Palette],
        [-1, 'unknown', ByteData, 64], # 64 bytes of unknown data.
        [-1, 'title_screen', Image, Image.PLANAR_8BIT, 32, 25, "title"],
        [-1, 'briefing', Palette],
        [-1, 'unknown', ByteData, 64], # 64 bytes of unknown data.
        [-1, 'mission_briefing', Image, Image.PLANAR_8BIT, 32, 24, "briefing"],
        [-1, 'intermission', Palette],
        [-1, 'intermission_background', Image, Image.PLANAR_4BIT, 8, 8, "intermission", 0x50],
        [-1, 'intermission_player', Image, Image.PLANAR_4BIT, 11, 33, "intermission", 0x00],
        [-1, 'intermission_mission', Image, Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_floor', Image, Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_complete', Image, Image.PLANAR_4BIT, 17, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_time', Image, Image.PLANAR_4BIT, 9, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_enemy', Image, Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_par', Image, Image.PLANAR_4BIT, 8, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_treasure', Image, Image.PLANAR_4BIT, 17, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_score', Image, Image.PLANAR_4BIT, 11, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_secret', Image, Image.PLANAR_4BIT, 13, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_bonus', Image, Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_perfect', Image, Image.PLANAR_4BIT, 15, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_speed', Image, Image.PLANAR_4BIT, 12, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_of', Image, Image.PLANAR_4BIT, 4, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_overall', Image, Image.PLANAR_4BIT, 15, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_colon', Image, Image.PLANAR_4BIT, 1, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_number_0', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_number_1', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_number_2', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_number_3', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_number_4', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_number_5', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_number_6', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_number_7', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_number_8', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_number_9', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_percent', Image, Image.PLANAR_4BIT, 2, 2, "intermission", 0x20, 0x20],
        [-1, 'intermission_exclamation', Image, Image.PLANAR_4BIT, 1, 2, "intermission", 0x20, 0x20],
        [-1, 'overhead_map_tiles', Image, Image.PLANAR_8BIT, 8, 5, "main"],
        [-1, 'main', Palette],
        [-1, 'unknown', ByteData, 0x2300], # Unknown data that's 0x2300 bytes long.
        [-1, 'status_bar_left_text', Image, Image.PLANAR_4BIT, 14, 1, "main", 0xf0, 0xf0],
        [-1, 'status_bar_percent', Image, Image.PLANAR_4BIT, 1, 2, "main", 0xf0, 0xf0],
        [-1, 'status_bar_right_text', Image, Image.PLANAR_4BIT, 11, 1, "main", 0xf0, 0xf0],
        [-1, 'status_bar', Image, Image.TILED_8BIT, 14, 2, "main"],
        [-1, 'font', Image, Image.PLANAR_4BIT, 16, 6, "main", 0xf0, 0xf0],
        [-1, 'status_bar_numbers', Image, Image.PLANAR_4BIT, 16, 2, "main", 0xf0, 0xf0],
        [-1, 'status_bar_faces', Image, Image.PLANAR_4BIT, 16, 8, "main", 0xf0, 0xf0],
        [-1, 'weapon_0', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
        [-1, 'weapon_1', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
        [-1, 'weapon_2', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
        [-1, 'weapon_3', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
        [-1, 'weapon_4', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
        [-1, 'weapon_5', Image, Image.PLANAR_4BIT, 16, 16, "main", 0xf0, 0xf0],
        ]
    entry_lists = [
        # class, count, offset lambda, naming lambda, [args...]
        # lambdas used for count must only have 'self' parameter.
        # lambdas for offset, naming, or args must have 'self, x'
        # Map offsets are stored as: 00 01 35 03 CC
        # final CC needs to be converted to be 0C
        # 00 01 appears to mark index entries.
        [ Map,
          lambda self: utils.store_and_get_length(self._map_offsets, self._rom.read_rom_address_list_wolf(0xfc886, 30)),
          lambda self, x: self._map_offsets[x],
          lambda self, x: 'Map ' + utils.insert_string(self._rom.read_text_chunk(0x3958 + x * 3, 2), 1, '-')],
        [ Image,
          64,
          lambda self, x: 0x20000 + x * 32 * 32,
          lambda self, x: 'wall_' + str(x),
          Image.LINEAR_8BIT, 32, 32, "main"],
        [ Sprite,
          lambda self: utils.store_and_get_length(self._sprites, Sprite.read_sprite_info_wolf3d(self._rom, 0xfda6e, 0x30000)),
          lambda self, x: self._sprites[x]['offset'],
          lambda self, x: 'sprite_' + str(x),
          lambda self, x: self._sprites[x]['column_count'],
          "main"],
        [ Sound,
          lambda self: utils.store_and_get_length(self._sounds, Sound.read_sound_info(self._rom, 0xe981e, 0xfc6b8, 5)),
          lambda self, x: self._sounds[x]['offset'],
          lambda self, x: 'sound_' + str(x),
          lambda self, x: self._sounds[x]['loop_offset']],
        ]
    _sounds = []
    _sprites = []
    _map_offsets = []
    _rom = None

    def __init__(self, rom):
        self._rom = rom
