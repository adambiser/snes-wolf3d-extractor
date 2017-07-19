import os
import sys
import timeit

from extractor import *
from extractor.entrytype import *

"""
TODO:
Text entries

Add tkinter
http://www.python-course.eu/tkinter_labels.php

Save Config
https://docs.python.org/2/library/configparser.html
https://martin-thoma.com/configuration-files-in-python/

Appdata path:
https://stackoverflow.com/questions/13584992/config-file-location-on-windows-create-directory-in-appdata
"""

ROM_FILE_NAME = "input\Wolfenstein 3D (USA).sfc"
##ROM_FILE_NAME = "input\Super Noah's Ark 3D (U) [!].smc"
##ROM_FILE_NAME = "input\Wolfenstein 3D (USA) (Beta 1).sfc"
##ROM_FILE_NAME = "input\Wolfenstein 3D (USA) (Beta 2).sfc"
##ROM_FILE_NAME = "input\Super Noah's Ark 3D (U) (2013).sfc"
##ROM_FILE_NAME = "input\Wolfenstein 3D (Europe).sfc"
ROM_FILE_NAME = "input\Wolfenstein 3D (Japan).sfc"

'''
Main program.
'''
def main():
    output_path = "output"
    with Rom(ROM_FILE_NAME) as rom:
        # Create rom-specific output path
        output_path += '_' + rom.rom_name #os.path.splitext(os.path.basename(rom.filename))[0]
        utils.create_path(output_path)
        # Testing
##        rom.get_entry(rom.get_entries_of_class(Song)[2]).save(output_path)
##        rom.get_entry(rom.get_entries_of_class(Song)[7]).save(output_path)
##        for s in rom.get_entries_of_class(Song):
##            print 'Writing song from entry {}'.format(s)
##            rom.get_entry(s).save(output_path)
##            break
##        sys.exit()
        # Load all maps from the ROM, covert them to DOS format, then save.
        gamemaps = [rom.get_entry(m).generate_dos_map() for m in rom.get_entries_of_class(Map)]
        Map.save_as_wdc_map_file(output_path + "/snes.map", gamemaps)
        for g in range(rom.get_entry_count()):
            # Skip byte data entries. They are unknowns.
##            if rom.get_entry_type(g) is ByteData:
##                continue
            # Skip maps. They were done first.
            if rom.get_entry_type(g) is Map:
                continue
            if rom.get_entry_type(g) is Song:
                continue
##            if not rom.get_entry_type(g) is Image:
##                continue
            entry = rom.get_entry(g)
            print '0x{:x} - {}'.format(entry.offset, entry.name)
            entry.save(output_path)

print 'time {}'.format(timeit.timeit(main, number=1))
