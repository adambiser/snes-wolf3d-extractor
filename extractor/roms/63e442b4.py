from . import wolf3d as base

def init(rom):
    base._rom_name = "Wolfenstein 3D (Beta 1)"
    base._starting_offset = 0x87280
    base._has_ball_texture = False
    base._map_offset_list_offset = 0xfb886
    base._map_name_offset = 0x3268
    base._sprite_info_offset = 0xfca47
    base._sound_info_offset_1 = 0xec44b
    base._sound_info_offset_2 = 0xfb6b8
    base._sound_group_2_count = 5
    base.init(rom)

