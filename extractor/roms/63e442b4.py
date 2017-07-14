import importlib
wolf3d = importlib.import_module('.6582a8f5', 'extractor.roms')

def init(rom):
    wolf3d._rom_name = "Wolfenstein 3D (Beta 1)"
    wolf3d._starting_offset = 0x87280
    wolf3d._has_ball_texture = False
    wolf3d._map_offset_list_offset = 0xfb886
    wolf3d._map_name_offset = 0x3268
    wolf3d._sprite_info_offset = 0xfca47
    wolf3d._sound_info_offset_1 = 0xec44b
    wolf3d._sound_info_offset_2 = 0xfb6b8
    wolf3d._sound_group_2_count = 5
    wolf3d.init(rom)

