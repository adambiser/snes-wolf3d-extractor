import struct
import textwrap
import typing

from .abstractentry import AbstractEntry
from .sound import Sound
if typing.TYPE_CHECKING:
    from ..rom import Rom


class InstrumentList(AbstractEntry):
    """The list of instruments used by the game to play music.

    Instrument information was found through some guess work and through spc dumps using snes9x.

    Note that this information also appears at 0xfd7de for the Instrument test screen, but this information is
    misleading and not used for song playback.  In fact, the Pitch Scale and Velocity Scale values on that screen do
    not seem to do anything at all, at least in an emulator.
    """

    def __init__(self, offset, name):
        super().__init__(offset, name)
        self.instruments = None

    def load(self, rom):
        # Only load once.
        if self.instruments is not None:
            return
        rom.seek(self.offset)
        # Load the instrument numbers and info offsets.
        self.instruments = {}
        has_another = True
        while has_another:
            instrument_number = rom.read_ubyte()
            b1 = rom.read_ubyte()
            assert b1 == 0
            b1 = rom.read_ubyte()
            if b1 == 0xf0:  # Relative offset
                info_offset = rom.read_ubyte() + 1
                info_offset += rom.tell()
            elif b1 == 0xd0:  # Absolute offset
                # No clue what this is.
                unknown = rom.read(2)
                assert unknown == b'\x03\x4c'
                info_offset = rom.read_ushort() + 1
            else:
                raise Exception(f'Unexpected value: {b1:#04x}')
            self.instruments[instrument_number] = Instrument(instrument_number, info_offset)
            has_another = (rom.read_ubyte() == 0xc9)
        # Load the instrument sound info.
        for info in self.instruments:
            self.instruments[info].load(rom)

    def save(self, path, filename=None, filetype=None):
        filename = self._get_filename(path, filename, self.name + '.txt')
        with open(filename, 'w') as f:
            f.write(str(self))

    def __getitem__(self, key):
        """Gets an instrument by MIDI instrument number."""
        return self.instruments[key]

    def __str__(self):
        return f'{len(self.instruments)} instruments:\n\n' + \
               '\n\n'.join([str(self.instruments[i]) for i in sorted(self.instruments)])


class Instrument:
    """An instrument based on a sound from the rom."""

    def __init__(self, instrument_number, info_offset):
        self.instrument_number = instrument_number
        self._info_offset = info_offset
        self.sound_number = None
        self.data = None
        self.loop_offset = None
        self.is_percussion = None
        self.pitch = None
        self.velocity = None

    def load(self, rom: "Rom"):
        sound_number = 0
        rom.seek(self._info_offset)
        b1 = rom.read_ubyte()
        b2 = rom.read_ubyte()
        if b2 == 0:  # In this cause, b1 is the sound number.
            sound_number = b1
            # No clue what this is.
            unknown = rom.read(2)
            assert unknown == b'\x85\x01'
            b2 = rom.read_ubyte()
        if b2 == 0xa9:  # Percussion
            # Next value is the pitch value to use no matter what midi note is given.
            self.is_percussion = True
            self.pitch = rom.read_ushort()
        elif b2 == 0xa5:  # Melodic
            self.is_percussion = False
            # No clue what this is.
            unknown = rom.read(4)
            assert unknown == b'\x0c\x0a\xaa\xbf'
            self.pitch = Instrument.read_ushort_list_at(rom, Instrument.read_3_byte_address(rom), 0x80)
        else:
            raise Exception('Unexpected value while loading instrument {}. '
                            'Tell: 0x{:x}. Value: 0x{:x}'.format(self.instrument_number, rom.tell(), b2))
        # No clue what this is.
        unknown = rom.read(5)
        assert unknown == b'\x85\x03\xa6\x0e\xbf'
        self.velocity = Instrument.read_ubyte_list_at(rom, Instrument.read_3_byte_address(rom), 0x80)
        # Load the sound data from the rom.
        sound_info = rom.get_entry(rom.get_entries_of_class(Sound)[sound_number]).get_wav_info()
        self.sound_number = sound_number
        self.data = sound_info['data']
        self.loop_offset = sound_info['loop_offset']

    @staticmethod
    def read_3_byte_address(rom: "Rom"):
        """Reads a 3 byte rom address (really 22-bit, not 24)."""
        return struct.unpack('<I', rom.read(3) + b'\00')[0] & 0x3fffff

    @staticmethod
    def read_ubyte_list_at(rom: "Rom", offset: int, length: int):
        """Reads a list of unsigned bytes from the rom and sets the rom position back to where it was."""
        previous_offset = rom.tell()
        rom.seek(offset)
        values = struct.unpack('<' + length * 'B', rom.read(length))
        rom.seek(previous_offset)
        return values

    @staticmethod
    def read_ushort_list_at(rom: "Rom", offset: int, length: int):
        """Reads a list of unsigned shorts from the rom and sets the rom position back to where it was."""
        previous_offset = rom.tell()
        rom.seek(offset)
        values = struct.unpack('<' + length * 'H', rom.read(length * 2))
        rom.seek(previous_offset)
        return values

    def __str__(self):
        text = f'{self.instrument_number} ({"percussion" if self.is_percussion else "melodic"}): ' \
               f'Sound {self.sound_number}, length: {len(self.data)}, loops at {self.loop_offset}\n'
        text += textwrap.fill(f'Pitch: {self.pitch}') + '\n'
        text += textwrap.fill(f'Velocity: {self.velocity}')
        return text
