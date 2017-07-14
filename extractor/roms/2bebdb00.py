from . import wolf3d as base

def init(rom):
    base._rom_name = "Wolfenstein 3D (Beta 2)"
    base._starting_offset = 0x82b7b
    base._has_ball_texture = True
    base._map_offset_list_offset = 0xfc086
    base._map_name_offset = 0x3935
    base._sprite_info_offset = 0xfd254
    base._sound_info_offset_1 = 0xe9436
    base._sound_info_offset_2 = 0xfbeb8
    base._sound_group_2_count = 5
    base.init(rom)

