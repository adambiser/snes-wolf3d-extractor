import binascii

from .roms import rom_info
from .utils import *


# Help for finding entries:
# First Map:
# - Search for "TELAS"
# - Go forward 0x38 bytes. This should be the offset of the first map.
# - Search for the hex values of this offset + 0xc00000.


class Rom:
    def __init__(self, filename):
        """The crc32 of the given file is used to determine which rom information to use."""
        self.f = None
        self.name = ''
        self.info = ''
        self.filename = filename
        self.offset_delta = 0
        self.filecrc32 = format(self.get_crc32(False), '8x')
        self.datacrc32 = format(self.get_crc32(True), '8x')
        self.entries = []
        # Load rom information into the rom object.
        with self:
            rom_info.init(self)
        print(f'Detected ROM: "{self.name}" (data crc32: {self.datacrc32}'
              f'{", file crc32: {self.filecrc32}" if self.filecrc32 != self.datacrc32 else ""})')

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *a):
        self.close()
        return False

    def get_crc32(self, detect_smc=False):
        """Calculates the unsigned crc32 value for the rom."""
        with self:
            if detect_smc:
                buf = struct.unpack(">H", self.read(2))[0]
                if buf == 0x8000:
                    self.offset_delta = 0x200
                self.seek(0, 0)
            buf = self.read()
        return binascii.crc32(buf) & 0xFFFFFFFF

    def open(self):
        """Opens the rom for reading."""
        self.f = open(self.filename, 'rb')

    def close(self):
        """Closes the rom's inner file object."""
        self.f.close()

    def read(self, size: int = -1) -> bytes:
        """Reads the given number of bytes from the rom."""
        return self.f.read(size)

    def read_ubyte(self) -> int:
        """Reads an unsigned byte."""
        return read_ubyte(self)

    def read_ushort(self) -> int:
        """Reads an unsigned short."""
        return read_ushort(self)

    def seek(self, offset, whence=0):
        """Move to a new position within the rom."""
        if whence == 0:
            offset += self.offset_delta
        self.f.seek(offset, whence)

    def tell(self) -> int:
        """Returns the current position within the rom."""
        return self.f.tell() - self.offset_delta

    def add_entry(self, entry):
        """Adds an entry to the entry list.

        If the entry's offset is -1, its offset will be calculated from the previous entry's offset and length.
        """
        if entry.offset == -1:
            entry.offset = self.entries[-1].offset + self.entries[-1]._get_length()
        self.entries.append(entry)

    def add_entry_list(self, entries):
        for entry in entries:
            self.add_entry(entry)

    def get_entry_list(self):
        return sorted((entry.offset, entry.__class__.__name__, entry.name) for entry in self.entries)

    def print_entry_list(self):
        """Prints the list of entries (offset and name) sorted by offset."""
        for e in self.get_entry_list():
            print(f'{e[0]:#0x} - {e[1]} - {e[2]}')

    def get_entry_count(self) -> int:
        """Returns the number of entries in the rom."""
        return len(self.entries)

    def get_entry_index(self, name: str) -> int:
        """Gets the index of an entry by name."""
        return [entry.name for entry in self.entries].index(name)

    def get_entry_type(self, index):
        """Gets an entry's type."""
        if isinstance(index, str):
            index = self.get_entry_index(index)
        return self.entries[index].__class__

    def get_entries_of_class(self, cls):
        """Gets a list of indices of entries of the given class."""
        return [x for x in range(len(self.entries)) if self.entries[x].__class__ is cls]

    def get_entry(self, index: int):
        """Loads and returns an entry from the rom."""
        if isinstance(index, str):
            index = self.get_entry_index(index)
        self.entries[index].load(self)
        return self.entries[index]

    def read_text_chunk(self, offset: int, length: int) -> str:
        """Gets text from an offset within the rom."""
        self.seek(offset)
        return self.read(length).decode("ascii")

    def read_rom_address(self) -> int:
        """Reads three bytes from the current location within the rom and converts it to an offset."""
        return (struct.unpack('<i', self.read(3) + b'\x00')[0] - 0xc00000) & 0xffffff

    def read_rom_address_from(self, lookup_offset: int) -> int:
        """Reads a rom address from an offset within the rom."""
        self.seek(lookup_offset)
        return self.read_rom_address()
