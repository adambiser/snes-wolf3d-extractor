# TODO
# 9c3869d0 - usa, but starts at 0x200 bytes

############################################
# Super 3D Noah's Ark
############################################
def rom_a2315a14(rom):
    from . import super_3d_noahs_ark as base
    base._rom_name = "Super 3D Noah's Ark (1994)"
    base.init(rom)

def rom_643d5097(rom):
    # The 2013 Steam release of SNA3D is the same as 1994 version
    # but with a newer copyright.
    from . import super_3d_noahs_ark as base
    base._rom_name = "Super 3D Noah's Ark (2013)"
    base.init(rom)

############################################
# Wolfenstein 3D
############################################
def rom_6582a8f5(rom):
    from . import wolfenstein_3d as base
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

def rom_6a455ee2(rom):
    from . import wolfenstein_3d as base
    base._rom_name = "Wolfenstein 3D (Europe)"
    base._starting_offset = 0x82ab3
    base._has_ball_texture = True
    base._map_offset_list_offset = 0xfc886
    base._map_name_offset = 0x3958
    base._sprite_info_offset = 0xfda6e
    base._sound_info_offset_1 = 0xe981e
    base._sound_info_offset_2 = 0xfc6b8
    base._sound_group_2_count = 5
    base._instrument_info_offset = 0x9c
    base._song_offset_list_offset = 0xfd7a1
    base.init(rom)
    
def rom_cc47b8f9(rom):
    from . import wolfenstein_3d as base
    base._rom_name = "Wolfenstein 3D (Japan)"
    base._starting_offset = 0x82ab3
    base._has_ball_texture = True
    base._map_offset_list_offset = 0xfc886
    base._map_name_offset = 0x3958
    base._sprite_info_offset = 0xfda6e
    base._sound_info_offset_1 = 0xe66de
    base._sound_info_offset_2 = 0xfc6b8
    base._sound_group_2_count = 5
    base._instrument_info_offset = 0x8b
    base._song_offset_list_offset = 0xfd7a1
    base._is_japan = True
    base.init(rom)
    
def rom_63e442b4(rom):
    from . import wolfenstein_3d as base
    base._rom_name = "Wolfenstein 3D (Beta 1)"
    base._starting_offset = 0x87280
    base._has_ball_texture = False
    base._map_offset_list_offset = 0xfb886
    base._map_name_offset = 0x3268
    base._sprite_info_offset = 0xfca47
    base._sound_info_offset_1 = 0xec44b
    base._sound_info_offset_2 = 0xfb6b8
    base._sound_group_2_count = 5
    base._instrument_info_offset = 0xd
    base._song_offset_list_offset = 0xFC77A
    base.init(rom)

def rom_2bebdb00(rom):
    from . import wolfenstein_3d as base
    base._rom_name = "Wolfenstein 3D (Beta 2)"
    base._starting_offset = 0x82b7b
    base._has_ball_texture = True
    base._map_offset_list_offset = 0xfc086
    base._map_name_offset = 0x3935
    base._sprite_info_offset = 0xfd254
    base._sound_info_offset_1 = 0xe9436
    base._sound_info_offset_2 = 0xfbeb8
    base._sound_group_2_count = 5
    base._instrument_info_offset = 0x8b
    base._song_offset_list_offset = 0xFCF87
    base.init(rom)

############################################
# Main init function.
############################################
def init(rom):
    globals()['rom_' + rom.crc32](rom)
