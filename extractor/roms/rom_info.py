from extractor.exceptions import RomInfoNotFoundError
from extractor.entrytype import *

"""
NOTE: Short text and error messages are not included.
Examples from Wolf3D USA:
    3301    0x0a    password_entry
    39EF    0x10    invalid_password
    42FA    0x16    demo_recording
    50F4    0x0a    password_2
    74E9    0x62    not_designed_for_your_snes
            0x2d    walk_bad_dir
    84A0    0x15    move_actoron_bad_dir
    95B7    0x10    static_overload
    9DA7    0x4a    bad_spawn_type
            0x10    bad_changeweapon
            0x8     bad_fire
    C0CE    0x13    pwall_seg
    DC90    0x13    bad_secret_elevator
    FFC0    0x16    wolfenstein_3d
    FF7E6   0x10b   error_messages  has_length_byte=True
"""

############################################
# Super 3D Noah's Ark
############################################
def rom_a2315a14(rom):
    from . import super_3d_noahs_ark as base
    rom.name = "Super 3D Noah's Ark (1994)"
    base.init(rom)

def rom_643d5097(rom):
    rom_a2315a14(rom)
    rom.name = "Super 3D Noah's Ark (2013)"
    rom.info = 'The 2013 Steam release is the same as 1994 version but with a newer copyright.'

############################################
# Wolfenstein 3D
############################################
def rom_6582a8f5(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (USA)"
    base.init(rom)
    rom.add_entry_list([
##        Text(0x394B, 0x66, 'level_select_screen'),
##        Text(0x3CD0, 0x42, 'password_screen'),
##        Text(0x3F5D, 0x6a, 'main_menu'),
        Text(0x5590, 0x15, 'meet_the_cast'),
        Text(0x5782, 0x1e4, 'credits'),
##        Text(0x65BC, 0xc9, 'sound_test'),
##        Text(0x6801, 0x57, 'music_test'),
##        Text(0x6B7A, 0x6f, 'instrument_test'),
        Text(0x739E, 0x77, 'copyright'),
        Text(0xFCCAF, 0x934, 'mission_briefing', '\x00\x01\\x2a|\x00\x01|\x00\x02'),
        Text(0xFD69F, 0x8d, 'cast_list', '\x00\x01'),
        ])

def rom_9c3869d0(rom):
    rom.offset_delta = 0x200
    rom_6582a8f5(rom)
    rom.name = "Wolfenstein 3D (USA) SMC"
    rom.info = 'The USA release but with an extra 0x200 bytes at the beginning of the file.'

def rom_6a455ee2(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (Europe)"
    base.init(rom,
              instrument_info_offset = 0x9c,
              )
    rom.add_entry_list([
##        Text(0x395C, 0x66, 'level_select_screen'),
##        Text(0x3CE1, 0x42, 'password_screen'),
##        Text(0x3F6E, 0x6a, 'main_menu'),
        Text(0x55A1, 0x15, 'meet_the_cast'),
        Text(0x5793, 0x1e4, 'credits'),
##        Text(0x65CE, 0xc9, 'sound_test'),
##        Text(0x6813, 0x57, 'music_test'),
##        Text(0x6B8C, 0x6f, 'instrument_test'),
        Text(0x73B0, 0x77, 'copyright'),
        Text(0xFCCAF, 0x934, 'mission_briefing', '\x00\x01\\x2a|\x00\x01|\x00\x02'),
        Text(0xFD69F, 0x8d, 'cast_list', '\x00\x01'),
        ])
              
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
