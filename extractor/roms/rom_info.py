# TODO
# 9c3869d0 - usa, but starts at 0x200 bytes

from extractor.exceptions import RomInfoNotFoundError

############################################
# Super 3D Noah's Ark
############################################
def rom_a2315a14(rom):
    from . import super_3d_noahs_ark as base
    rom.name = "Super 3D Noah's Ark (1994)"
    base.init(rom)

def rom_643d5097(rom):
    from . import super_3d_noahs_ark as base
    rom.name = "Super 3D Noah's Ark (2013)"
    rom.info = 'The 2013 Steam release is the same as 1994 version but with a newer copyright.'
    base.init(rom)

############################################
# Wolfenstein 3D
############################################
def rom_6582a8f5(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (USA)"
    base.init(rom)

def rom_9c3869d0(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (USA) SMC"
    rom.info = 'The USA release but with an extra 0x200 bytes at the beginning of the file.'
    rom.offset_delta = 0x200
    base.init(rom)

def rom_6a455ee2(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (Europe)"
    base.init(rom,
              instrument_info_offset = 0x9c,
              )
              
def rom_cc47b8f9(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (Japan)"
    base.init(rom,
              sound_info_offset_1 = 0xe66de,
              is_japan = True,
              )
    
def rom_63e442b4(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (Beta 1)"
    base.init(rom,
              starting_offset = 0x87280,
              has_ball_texture = False,
              map_offset_list_offset = 0xfb886,
              map_name_offset = 0x3268,
              sprite_info_offset = 0xfca47,
              sound_info_offset_1 = 0xec44b,
              sound_info_offset_2 = 0xfb6b8,
              instrument_info_offset = 0xd,
              song_offset_list_offset = 0xFC77A,
              )

def rom_2bebdb00(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (Beta 2)"
    base.init(rom,
              starting_offset = 0x82b7b,
              has_ball_texture = True,
              map_offset_list_offset = 0xfc086,
              map_name_offset = 0x3935,
              sprite_info_offset = 0xfd254,
              sound_info_offset_1 = 0xe9436,
              sound_info_offset_2 = 0xfbeb8,
              song_offset_list_offset = 0xFCF87,
              )

############################################
# Main init function.
############################################
def init(rom):
    try:
        globals()['rom_' + rom.crc32](rom)
    except KeyError as e:
        raise RomInfoNotFoundError(rom.crc32)
