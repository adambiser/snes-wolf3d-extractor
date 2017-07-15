from . import AbstractEntry
from .sound import Sound
import struct

class InstrumentList(AbstractEntry):
    """The list of instruments used by the game to play music.

    Instrument information was found through some guess work and through
    spc dumps using snes9x
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
        instr_info = []
        has_another = True
        while has_another:
            instr_info.append({})
            info = instr_info[-1]
            info['instrument_number'] = rom.read_ubyte()
            b1 = rom.read_ubyte()
            assert b1 == 0
            b1 = rom.read_ubyte()
            if b1 == 0xf0:
                info['info_offset'] = rom.read_ubyte() + 1
                info['info_offset'] += rom.tell()
            elif b1 == 0xd0:
                b1 = rom.read_ubyte()
                assert b1 == 0x03
                b1 = rom.read_ubyte()
                assert b1 == 0x4c
                info['info_offset'] = rom.read_ushort() + 1
            else:
                raise Exception('Unexpected value: ' + hex(b1))
            has_another = (rom.read_ubyte() == 0xc9)
        # Read instrument sound info.
        sound_number = 0
        for info in instr_info:
            rom.seek(info['info_offset'])
            b1 = rom.read_ubyte()
            b2 = rom.read_ubyte()
            if b2 == 0: # b1 is a new sound number
                sound_number = b1
                b1 = rom.read_ubyte()
                assert b1 == 0x85
                b1 = rom.read_ubyte()
                assert b1 == 0x01
                b2 = rom.read_ubyte()
            if b2 == 0xa9: # Percussion
                # Next value is the pitch value to use no matter what midi note is given.
                info['is_percussion'] = True
                info['pitch'] = rom.read_ushort()
            elif b2 == 0xa5: # Melodic
                info['is_percussion'] = False
                b1 = rom.read_ubyte()
                assert b1 == 0x0c
                b1 = rom.read_ubyte()
                assert b1 == 0x0a
                b1 = rom.read_ubyte()
                assert b1 == 0xaa
                b1 = rom.read_ubyte()
                assert b1 == 0xbf
                info['pitch'] = self.read_3_byte_address(rom)
            else:
                raise Exception('Unexpected value: ' + hex(b2))
            b1 = rom.read_ubyte()
            assert b1 == 0x85
            b1 = rom.read_ubyte()
            assert b1 == 0x03
            b1 = rom.read_ubyte()
            assert b1 == 0xa6
            b1 = rom.read_ubyte()
            assert b1 == 0x0e
            b1 = rom.read_ubyte()
            assert b1 == 0xbf
            info['velocity'] = rom.read_rom_address()
            info['sound_number'] = sound_number
        # Now create the instrument objects from all the info we have.
        self.instruments = {}
        sound_indices = rom.get_entries_of_class(Sound)
        for info in instr_info:
            instrument = Instrument()
            instrument.instrument_number = info['instrument_number']
            sound_info = rom.get_entry(sound_indices[info['sound_number']]).get_wav_info()
            instrument.sound_data = sound_info['data']
            instrument.sound_loop_offset = sound_info['loop_offset']
            instrument.is_percussion = info['is_percussion']
            if instrument.is_percussion:
                instrument.pitch = info['pitch']
            else:
                instrument.pitch = self.read_ushort_table_at(rom, info['pitch'], 0x80)
            instrument.velocity = self.read_ubyte_table_at(rom, info['velocity'], 0x80)
            self.instruments[info['instrument_number']] = instrument
##            print instrument.instrument_number, len(instrument.sound_data)

    def save(self, path, filename=None, filetype=None):
        """There is no save functionality defined for this entry type. Yet."""
##        filename = self._get_filename(path, filename, self.name + '.txt')
        pass

    def read_3_byte_address(self, rom):
        return struct.unpack('<I', rom.read(3) + '\00')[0] & 0x3fffff

    def read_ubyte_table_at(self, rom, offset, length):
        previous_offset = rom.tell()
        rom.seek(offset)
        table = struct.unpack('<' + length * 'B', rom.read(length))
        rom.seek(previous_offset)
        return table

    def read_ushort_table_at(self, rom, offset, length):
        previous_offset = rom.tell()
        rom.seek(offset)
        table = struct.unpack('<' + length * 'H', rom.read(length * 2))
        rom.seek(previous_offset)
        return table

class Instrument:
    """An instrument based on a sound from the rom."""
    instrument_number = None
    sound_data = None
    sound_loop_offset = None
    is_percussion = None
    pitch = None
    velocity = None

    def __init__(self):
        pass

    def load(self, info_offset):
        
        
