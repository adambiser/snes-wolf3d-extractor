from . import wolf3d as base

def init(rom):
    base._rom_name = "Wolfenstein 3D (USA)"
    base._starting_offset = 0x82ab3
    base._has_ball_texture = True
    base._map_offset_list_offset = 0xfc886
    base._map_name_offset = 0x3958
    base._sprite_info_offset = 0xfda6e
    base._sound_info_offset_1 = 0xe981e
    base._sound_info_offset_2 = 0xfc6b8
    base._sound_group_2_count = 5
    base._instrument_info_offset = 0x8b
    base._song_offset_list_offset = 0xfd7a1
    base.init(rom)
