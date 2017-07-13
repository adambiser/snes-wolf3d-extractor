from entry import Entry
from ..utils import *
from ..wav import wav

class Sound(Entry):
    loop_offset = None
    # Configuration constants
    SAMPLE_RATE = 11025

    '''
    Constructor.
    Loads brr sound data from the current position within the rom.
    '''
    def __init__(self, rom, name, loop_offset=None):
        Entry.__init__(self, rom, name)
        self.loop_offset = loop_offset
        print 'start: {:x}'.format(rom.tell())
        self.brr = self.read_brr_data(rom)
        print 'finish: {:x}'.format(rom.tell())
        print '{} has {} blocks'.format(name, len(self.brr))

    '''
    Returns a dictionary of the sound offsets.
    "data" is the offsets for all sounds.
    "loop" is the offsets of the loop position within the sound data.
    '''
    @staticmethod
    def read_sound_info(rom, sound_info_offset_1, sound_info_offset_2, sounds_2_count):
        # Load information for the first group of sounds.
        rom.seek(sound_info_offset_1)
        last_sound_1_offset = read_ushort(rom)
        # Not sure what this value really means, but it works.
        offset_delta = read_ushort(rom)
        # Skip to offset list.
        print 'reading sound group 1 at {:x}'.format(rom.tell())
        print 'last_sound_1_offset: {:x}'.format(last_sound_1_offset)
        rom.seek(0x400, 1)
        sounds = []
        while True:
            # Adjust offsets by given delta.
            data_offset = read_ushort(rom) - offset_delta
            if data_offset == last_sound_1_offset:
                break
            sounds.append({})
            sound = sounds[-1]
            # Convert data offset to a file offset.
            sound['offset'] = sound_info_offset_1 + 4 + data_offset
            # Convert loop offset to offset within sound data.
            sound['loop_offset'] = read_ushort(rom) - offset_delta - data_offset
        print 'found {} sounds'.format(len(sounds))
        print sounds
        # Load information for the second group of sounds.
        # There are 4 unknown bytes between these groups.
        first_sound_2_offset = sound_info_offset_1 + 4 + last_sound_1_offset + 4
        rom.seek(sound_info_offset_2)
        print 'reading sound group 2 at {:x}'.format(rom.tell())
        # First offset is 0.
        sounds.append({})
        sound = sounds[-1]
        sound['offset'] = first_sound_2_offset + 0
        sound['loop_offset'] = 0 # Never loops.
        # Now read shorts until another 0 is found.
        for x in range(sounds_2_count):
            sounds.append({})
            sound = sounds[-1]
            sound['offset'] = first_sound_2_offset + read_ushort(rom)
            sound['loop_offset'] = 0 # Never loops.
        print 'total: {} sounds'.format(len(sounds))
        return sounds

    '''
    Reads raw BRR data for the sound at the current position in the rom.
    '''
    @staticmethod
    def read_brr_data(rom):
        end_flag = 0
        brr = []
        while True:
            brr.append(struct.unpack('9B', rom.read(9)))
            # check for end flag.
            if brr[-1][0] & 1:
                break
        return brr

    '''
    Converts an unsigned nibble to a signed nibble.
    '''
    @staticmethod
    def signed_nibble(x):
        return (x | ~7) if (x & 8) else (x & 7)

    '''
    Clamps a signed short to be within its upper and lower bounds.
    '''
    @staticmethod
    def clamp_short(x):
        return -32768 if x < -32768 else 32767 if x > 32767 else x

    '''
    Converts the brr sound data to raw 16-bit WAV data.
    '''
    def get_wav_info(self):
        nibble = [0, 0]
        end_flag = 0
        data = []
        looping = False
        for block in self.brr:
            end_flag = (block[0] & 1) != 0
            loop_flag = (block[0] & 2) != 0
            if loop_flag and not looping:
                looping = True
            chunk_filter = (block[0] >> 2) & 3
            chunk_range = (block[0] >> 4)
            for b in block[1:]:
                nibble[0] = Sound.signed_nibble(b >> 4)
                nibble[1] = Sound.signed_nibble(b & 0xf)
                for n in range(2):
                    out = (nibble[n] << chunk_range)
                    #if chunk_filter == 0:
                    if chunk_filter == 1:
                        out += (15 / 16.0) * data[-1]
                    elif chunk_filter == 2:
                        out += (61 / 32.0) * data[-1] - (15 / 16.0) * data[-2]
                    elif chunk_filter == 3: 
                        out += (115 / 64.0) * data[-1] - (13 / 16.0) * data[-2]
                    # clamp to 16-bit signed short.
                    data.append(Sound.clamp_short(int(out)))
        return {
            'data': data,
            'looping': looping,
            'loop_offset': (self.loop_offset / 9) * 16 if looping else None
            }

    '''
    Saves the given sound information to a WAV file.
    '''
    def save(self, filename):
        data = self.get_wav_info()
        with open(filename, 'wb') as f:
            w = wav.Writer(Sound.SAMPLE_RATE, 1, 16)
            w.write(f, data['data'], data.get('loop_offset'))

    '''
    Returns the default file extension to use while saving.
    Should begin with the period.
    '''
    def get_default_extension(self):
        return ".wav"
