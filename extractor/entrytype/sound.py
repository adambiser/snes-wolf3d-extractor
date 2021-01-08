import struct
import typing

from .abstractentry import AbstractEntry
from ..wav import wav
if typing.TYPE_CHECKING:
    from ..rom import Rom


class Sound(AbstractEntry):
    # Configuration constants
    SAMPLE_RATE = 11025

    def __init__(self, offset, name, loop_offset=None):
        super().__init__(offset, name)
        self.loop_offset = loop_offset
        self.brr = None

    def load(self, rom):
        rom.seek(self.offset)
        self.brr = Sound.read_brr_data(rom)

    def save(self, path, filename=None, filetype=None):
        """Saves the sound as a WAV file."""
        data = self.get_wav_info()
        filename = self._get_filename(path, filename, self.name + '.wav')
        with open(filename, 'wb') as f:
            w = wav.Writer(Sound.SAMPLE_RATE, 1, 16)
            w.write(f, data['data'], data.get('loop_offset'))

    @staticmethod
    def read_sound_info(rom: "Rom", sound_info_offset_1: int, sound_info_offset_2: int, sounds_2_count: int):
        """Returns an array of sound offset dicts.

        For each sound offset dict:
        'offset' - The offset of the sound within the rom.
        'loop_offset' - The loop start offset within the brr data.
        """
        # Load information for the first group of sounds.
        rom.seek(sound_info_offset_1)
        last_sound_1_offset = rom.read_ushort()
        # Not sure what this value really means, but it works.
        offset_delta = rom.read_ushort()
        # Skip to offset list.
        # print(f'reading sound group 1 at {rom.tell():#0x}')
        # print(f'last_sound_1_offset: {last_sound_1_offset:#0x}')
        rom.seek(0x400, 1)
        sounds = []
        while True:
            # Adjust offsets by given delta.
            data_offset = rom.read_ushort() - offset_delta
            if data_offset == last_sound_1_offset:
                break
            sounds.append({})
            sound = sounds[-1]
            # Convert data offset to a file offset.
            sound['offset'] = sound_info_offset_1 + 4 + data_offset
            # Convert loop offset to offset within sound data.
            sound['loop_offset'] = rom.read_ushort() - offset_delta - data_offset
        # print(f'found {len(sounds)} sounds')
        # print(sounds)
        # Load information for the second group of sounds.
        # There are 4 unknown bytes between these groups.
        first_sound_2_offset = sound_info_offset_1 + 4 + last_sound_1_offset + 4
        rom.seek(sound_info_offset_2)
        # print(f'reading sound group 2 at {rom.tell():#0x}')
        # First offset is 0.
        sounds.append({})
        sound = sounds[-1]
        sound['offset'] = first_sound_2_offset + 0
        sound['loop_offset'] = 0  # Never loops.
        # Now read shorts until another 0 is found.
        for x in range(sounds_2_count):
            sounds.append({})
            sound = sounds[-1]
            sound['offset'] = first_sound_2_offset + rom.read_ushort()
            sound['loop_offset'] = 0  # Never loops.
        # print(f'found {len(sounds)} sounds')
        return sounds

    @staticmethod
    def read_brr_data(rom: "Rom"):
        """Reads raw BRR data for the sound at the current position in the rom."""
        brr = []
        while True:
            brr.append(struct.unpack('9B', rom.read(9)))
            # check for end flag.
            if brr[-1][0] & 1:
                break
        return brr

    @staticmethod
    def signed_nibble(x: int):
        """Converts an unsigned nibble to a signed nibble."""
        return (x | ~7) if (x & 8) else (x & 7)

    def get_wav_info(self):
        """Converts the brr sound data to raw 16-bit WAV data.

        Returns a dict with the following entries:
        'data' - The converted WAV data.
        'looping' - When True, the sound loops.
        'loop_offset' - Offset to the loop start within the WAV data.
        """
        nibble = [0, 0]
        # end_flag = 0
        data = []
        looping = False
        for block in self.brr:
            # end_flag = (block[0] & 1) != 0
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
                    # if chunk_filter == 0:
                    if chunk_filter == 1:
                        out += (15 / 16.0) * data[-1]
                    elif chunk_filter == 2:
                        out += (61 / 32.0) * data[-1] - (15 / 16.0) * data[-2]
                    elif chunk_filter == 3: 
                        out += (115 / 64.0) * data[-1] - (13 / 16.0) * data[-2]
                    # clamp to 16-bit signed short.
                    data.append(wav.clamp_short(int(out)))
        return {
            'data': data,
            'looping': looping,
            'loop_offset': (self.loop_offset // 9) * 16 if looping else None
            }
