from . import AbstractEntry
from .sound import Sound
import struct
import textwrap

class InstrumentList(AbstractEntry):
    """The list of instruments used by the game to play music.

    Instrument information was found through some guess work and through
    spc dumps using snes9x.
    """
    instruments = None

    def __init__(self, offset, name):
        AbstractEntry.__init__(self, offset, name)

    def load(self, rom):
        # Only load once.
        if not self.instruments is None:
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
            if b1 == 0xf0: # Relative offset
                info_offset = rom.read_ubyte() + 1
                info_offset += rom.tell()
            elif b1 == 0xd0: # Absolute offset
                # No clue what this is.
                unknown = rom.read(2)
                assert unknown == '\x03\x4c'
                info_offset = rom.read_ushort() + 1
            else:
                raise Exception('Unexpected value: ' + hex(b1))
            self.instruments[instrument_number] = Instrument(instrument_number, info_offset)
            has_another = (rom.read_ubyte() == 0xc9)
        # Load the instrument sound info.
        for info in self.instruments:
            self.instruments[info].load(rom)

    def save(self, path, filename=None, filetype=None):
        """There is no save functionality defined for this entry type. Yet."""
        filename = self._get_filename(path, filename, self.name + '.txt')
        with open(filename, 'w') as f:
            f.write(str(self))

    def __str__(self):
        return '{} instruments:\n\n'.format(len(self.instruments)) + '\n\n'.join([str(self.instruments[i]) for i in sorted(self.instruments)])

class Instrument:
    """An instrument based on a sound from the rom."""
    _info_offset = None
    instrument_number = None
    sound_number = None
    sound_data = None
    sound_loop_offset = None
    is_percussion = None
    pitch = None
    velocity = None

    def __init__(self, instrument_number, info_offset):
        self.instrument_number = instrument_number
        self._info_offset = info_offset

    def load(self, rom):
        sound_number = 0
        rom.seek(self._info_offset)
        b1 = rom.read_ubyte()
        b2 = rom.read_ubyte()
        if b2 == 0: # In this cause, b1 is the sound number.
            sound_number = b1
            # No clue what this is.
            unknown = rom.read(2)
            assert unknown == '\x85\x01'
            b2 = rom.read_ubyte()
        if b2 == 0xa9: # Percussion
            # Next value is the pitch value to use no matter what midi note is given.
            self.is_percussion = True
            self.pitch = rom.read_ushort()
        elif b2 == 0xa5: # Melodic
            self.is_percussion = False
            # No clue what this is.
            unknown = rom.read(4)
            assert unknown == '\x0c\x0a\xaa\xbf'
            self.pitch = self.read_ushort_list_at(rom, self.read_3_byte_address(rom), 0x80)
        else:
            raise Exception('Unexpected value while loading instrument {}. Tell: 0x{:x}. Value: 0x{:x}'.format(self.instrument_number, rom.tell(), b2))
        # No clue what this is.
        unknown = rom.read(5)
        assert unknown == '\x85\x03\xa6\x0e\xbf'
        self.velocity = self.read_ubyte_list_at(rom, self.read_3_byte_address(rom), 0x80)
        # Load the sound data from the rom.
        sound_info = rom.get_entry(rom.get_entries_of_class(Sound)[sound_number]).get_wav_info()
        self.sound_number = sound_number
        self.sound_data = sound_info['data']
        self.sound_loop_offset = sound_info['loop_offset']

    def read_3_byte_address(self, rom):
        """Reads a 3 byte rom address (22-bit)."""
        return struct.unpack('<I', rom.read(3) + '\00')[0] & 0x3fffff

    def read_ubyte_list_at(self, rom, offset, length):
        """Reads a list of unsigned bytes from the rom and sets the position
        back to where it was before reading then.
        """
        previous_offset = rom.tell()
        rom.seek(offset)
        values = struct.unpack('<' + length * 'B', rom.read(length))
        rom.seek(previous_offset)
        return values

    def read_ushort_list_at(self, rom, offset, length):
        """Reads a list of unsigned shorts from the rom and sets the position
        back to where it was before reading then.
        """
        previous_offset = rom.tell()
        rom.seek(offset)
        values = struct.unpack('<' + length * 'H', rom.read(length * 2))
        rom.seek(previous_offset)
        return values

    def __str__(self):
        text = '{} ({}): Sound {}, length: {}, loops at {}\n'.format(self.instrument_number,
                                                                     'percussion' if self.is_percussion else 'melodic',
                                                                     self.sound_number,
                                                                     len(self.sound_data),
                                                                     self.sound_loop_offset)
        text += textwrap.fill('Pitch: {}'.format(self.pitch)) + '\n'
        text += textwrap.fill('Velocity: {}'.format(self.velocity))
        return text
