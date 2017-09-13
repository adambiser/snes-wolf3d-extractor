from extractor.exceptions import RomInfoNotFoundError
from extractor.entrytype import *


############################################
# Super 3D Noah's Ark
############################################


def rom_a2315a14(rom):
    from . import super_3d_noahs_ark as base
    rom.name = "Super 3D Noah's Ark (1994)"
    base.init(rom)
    rom.add_entry_list([
        Text(0xFCBEC, 0x170, 'story_1'),
        Text(0xFCDAB, 0x18f, 'story_2'),
        Text(0xFCF7D, 0x131, 'story_3'),
        Text(0xFD0ED, 0x126, 'story_4'),
        Text(0xFD24A, 0xd7, 'story_5'),
        Text(0xFD358, 0x106, 'story_6'),
        Text(0xFD50B, 0x7d, 'cast_list'),
        Text(0xFD5A1, 0x34, 'meet_the_cast'),
        Text(0xFD6ED, 0x188, 'credits'),
        ])


def rom_643d5097(rom):
    rom_a2315a14(rom)
    rom.name = "Super 3D Noah's Ark (2013)"
    rom.info = 'The 2013 Steam release is the same as 1994 version but with a newer copyright.'


def rom_7c4db7e3(rom):
    rom_a2315a14(rom)
    rom.name = "Super 3D Noah's Ark (h1C)"
    rom.info = 'h1C hack'


def rom_f8662282(rom):
    rom_a2315a14(rom)
    rom.name = "Super 3D Noah's Ark (h2C)"
    rom.info = 'h2C hack'


############################################
# Wolfenstein 3D
############################################


def rom_6582a8f5(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (USA)"
    base.init(rom)
    rom.add_entry_list([
        # Text(0x394B, 0x66, 'level_select_screen'),
        # Text(0x3CD0, 0x42, 'password_screen'),
        # Text(0x3F5D, 0x6a, 'main_menu'),
        Text(0x5590, 0x15, 'meet_the_cast'),
        Text(0x5782, 0x1e4, 'credits'),
        # Text(0x65BC, 0xc9, 'sound_test'),
        # Text(0x6801, 0x57, 'music_test'),
        # Text(0x6B7A, 0x6f, 'instrument_test'),
        Text(0x739E, 0x77, 'copyright'),
        Text(0xFCCAF, 0x934, 'mission_briefing', '\x00\x01\\x2a|\x00\x01|\x00\x02'),
        Text(0xFD69F, 0x8d, 'cast_list', '\x00\x01'),
        ])


def rom_6a455ee2(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (Europe)"
    base.init(rom,
              instrument_info_offset=0x9c,
              )
    rom.add_entry_list([
        Text(0x55A1, 0x15, 'meet_the_cast'),
        Text(0x5793, 0x1e4, 'credits'),
        Text(0x73B0, 0x77, 'copyright'),
        Text(0xFCCAF, 0x934, 'mission_briefing', '\x00\x01\\x2a|\x00\x01|\x00\x02'),
        Text(0xFD69F, 0x8d, 'cast_list', '\x00\x01'),
        ])


def rom_cc47b8f9(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (Japan)"
    base.init(rom,
              sound_info_offset_1=0xe66de,
              is_japan=True,
              )
    rom.add_entry_list([
        Text(0x55CA, 0x15, 'meet_the_cast'),
        Text(0x57BC, 0x1e4, 'credits'),
        Text(0x73BF, 0x5d, 'copyright'),
        Text(0xFCCAF, 0x934, 'mission_briefing', '\x00\x01\\x2a|\x00\x01|\x00\x02'),
        Text(0xFD69F, 0x8d, 'cast_list', '\x00\x01'),
        ])


def rom_63e442b4(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (Beta 1)"
    base.init(rom,
              starting_offset=0x87280,
              has_ball_texture=False,
              map_offset_list_offset=0xfb886,
              map_name_offset=0x3268,
              sprite_info_offset=0xfca47,
              sound_info_offset_1=0xec44b,
              sound_info_offset_2=0xfb6b8,
              instrument_info_offset=0xd,
              song_offset_list_offset=0xFC77A,
              )
    rom.add_entry_list([
        Text(0x4A94, 0x5e, 'rank'),
        Text(0x4D4F, 0x1a, 'meet_the_cast'),
        Text(0x4F01, 0x1bd, 'credits'),
        Text(0xFBCAD, 0x923, 'mission_briefing', '\x00\x01\\x2a|\x00\x01|\x00\x02'),
        Text(0xFC68F, 0x6e, 'cast_list', '\x00\x01'),
        ])


def rom_2bebdb00(rom):
    from . import wolfenstein_3d as base
    rom.name = "Wolfenstein 3D (Beta 2)"
    base.init(rom,
              starting_offset=0x82b7b,
              map_offset_list_offset=0xfc086,
              map_name_offset=0x3935,
              sprite_info_offset=0xfd254,
              sound_info_offset_1=0xe9436,
              sound_info_offset_2=0xfbeb8,
              song_offset_list_offset=0xFCF87,
              )
    rom.add_entry_list([
        Text(0x5473, 0x1a, 'meet_the_cast'),
        Text(0x5660, 0x1e4, 'credits'),
        Text(0x721C, 0x14, 'licensed'),
        Text(0xFC4AC, 0x932, 'mission_briefing', '\x00\x01\\x2a|\x00\x01|\x00\x02'),
        Text(0xFCE97, 0x7b, 'cast_list', '\x00\x01'),
        ])


def rom_4352c116(rom):
    rom_63e442b4(rom)
    rom.name = "Wolfenstein 3D (Beta 1 h1C)"
    rom.info = "h1C hack"


def rom_a8c264da(rom):
    rom_6582a8f5(rom)
    rom.name = "Wolfenstein 3D (German)"
    rom.info = "Fan-made German translation"


############################################
# Main init function.
############################################


def init(rom):
    try:
        globals()['rom_' + rom.datacrc32](rom)
    except KeyError as e:
        raise RomInfoNotFoundError(rom.datacrc32 + ("file: " + rom.filecrc32 if rom.filecrc32 != rom.filecrc32 else ""))
