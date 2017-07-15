from entrytype import *
import binascii
import struct
import utils
from importlib import import_module
from utils import *

'''
Help for finding entries:
First Map:
- Search for "TELAS"
- Go forward 0x38 bytes. This should be the offset of the first map.
- Search for the hex values of this offset + 0xc00000.
'''

class Rom:
    crc32 = None
    filename = None
    rom_name = None
    entries = []

    def __init__(self, filename):
        """The crc32 of the given file is used to determine which rom information to use."""
        # 2bebdb00 - beta 2
        # 9c3869d0 - usa, but starts at 0x200 bytes
        # 6a455ee2 - europe
        # cc47b8f9 - japan
        # Detect what rom was given.
        self.filename = filename
        self.crc32 = format(self.get_crc32(), '8x')
##        try:
        rom_info = import_module('.' + self.crc32, 'extractor.roms')
##        except ImportError:
##            raise Exception('Did not find ROM information for "{}" (crc32: {})'.format(filename, self.crc32))
        # Load rom information into the rom object.
        with self:
            rom_info.init(self)
        print 'Detected ROM: "{}" (crc32: {})'.format(self.rom_name, self.crc32)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *a):
        self.close()
        return False

    def get_crc32(self):
        """Calculates the unsigned crc32 value for the rom."""
        with self:
            buf = self.read()
        return (binascii.crc32(buf) & 0xFFFFFFFF)

    def open(self):
        """Opens the rom for reading."""
        self.f = open(self.filename, 'rb')

    def close(self):
        """Closes the rom's inner file object."""
        self.f.close()

    def read(self, size=-1):
        """Reads the given number of bytes from the rom."""
        return self.f.read(size)

    def read_ubyte(self):
        """Reads an unsigned byte."""
        return read_ubyte(self)

    def read_ushort(self):
        """Reads an unsigned short."""
        return read_ushort(self)

    def seek(self, offset, whence=0):
        """Move to a new position within the rom."""
        self.f.seek(offset, whence)

    def tell(self):
        """Returns the current position within the rom."""
        return self.f.tell()

    def add_entry(self, entry):
        """Adds an entry to the entry list.

        If the entry's offset is -1, its offset will be calculated from the previous entry's offset and length.
        """
        if entry.offset == -1:
            entry.offset = self.entries[-1].offset + self.entries[-1]._get_length()
        self.entries.append(entry)

    def print_entry_list(self):
        """Prints the list of entries (offset and name) sorted by offset."""
        entries = sorted((entry.offset, entry.__class__.__name__, entry.name) for entry in self.entries)
        for e in entries:
            print '0x{:x} - {} - {}'.format(e[0], e[1], e[2])

    def get_entry_count(self):
        """Returns the number of entries in the rom."""
        return len(self.entries)

    def get_entry_index(self, name):
        """Gets the index of an entry by name."""
        return [entry.name for entry in self.entries].index(name)

    def get_entry_type(self, index):
        """Gets an entry's type."""
        if isinstance(index, basestring):
            index = self.get_entry_index(index)
        return self.entries[index].__class__

    def get_entries_of_class(self, cls):
        """Gets a list of indices of entries of the given class."""
        return [x for x in range(len(self.entries)) if self.entries[x].__class__ is cls]

    def get_entry(self, index):
        """Loads and returns an entry from the rom."""
        if isinstance(index, basestring):
            index = self.get_entry_index(index)
        self.entries[index].load(self)
        return self.entries[index]

    def read_text_chunk(self, offset, length):
        """Gets text from an offset within the rom."""
        self.seek(offset)
        return self.read(length)

    def read_rom_address(self):
        """Reads three bytes from the current location within the rom and converts it to an offset."""
        return (struct.unpack('<i', self.read(3) + '\x00')[0] - 0xc00000) & 0xffffff

    def read_rom_address_from(self, lookup_offset):
        """Reads a rom address from an offset within the rom."""
        self.seek(lookup_offset)
        return self.read_rom_address()
