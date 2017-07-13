import os
import sys

from extractor import *
from extractor.entrytype import *

ROM_FILE_NAME = "..\ROMs\Wolfenstein 3D (USA).sfc"
##ROM_FILE_NAME = "..\ROMs\Super Noah's Ark 3D (U) [!].smc"
ROM_FILE_NAME = "..\ROMs\Wolfenstein 3D (USA) (Beta).sfc"
output_path = "output"

'''
Main program.
'''
with Rom(ROM_FILE_NAME) as rom:
##    rom.print_entry_list()
##    sys.exit()
    output_path += '_' + rom.rom_name #os.path.splitext(os.path.basename(rom.filename))[0]
    utils.create_path(output_path)
##    for s in rom.get_entries_of_class(Sound):
##        entry = rom.get_entry(s)
##        print '0x{:x} - {}'.format(entry.offset, entry.name)
##        entry.save(output_path + "/" + entry.get_default_filename())
##    sys.exit()
    # Load all maps from the ROM, covert them to DOS format, then save.
    gamemaps = [rom.get_entry(m).generate_dos_map() for m in rom.get_entries_of_class(Map)]
    Map.save_as_wdc_map_file(output_path + "/snes.map", gamemaps)
    for g in range(rom.get_entry_count()):
        # Skip byte data entries. They are unknowns.
        if rom.get_entry_type(g) is ByteData:
            continue
        # Skip maps. They were done first.
        if rom.get_entry_type(g) is Map:
            continue
        entry = rom.get_entry(g)
        print '0x{:x} - {}'.format(entry.offset, entry.name)
        entry.save(output_path + "/" + entry.name + entry.get_default_extension())
##        break
