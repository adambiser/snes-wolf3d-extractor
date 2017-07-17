from ..utils import *

def clamp_short(x):
    """Clamps a signed short to be within its upper and lower bounds."""
    return -32768 if x < -32768 else 32767 if x > 32767 else x

class Writer:
    # Configuration constants
    INCLUDE_LOOP_CUE_CHUNK_IN_WAV = True
    INCLUDE_LOOP_SMPL_CHUNK_IN_WAV = True

    def __init__(self, sample_rate,
                 channels,
                 bits_per_sample):
        self.sample_rate = sample_rate
        self.channels = channels
        self.bits_per_sample = bits_per_sample
        self.bytes_per_sample = self.bits_per_sample / 8

    def write(self, file, sound_data, loop_offset=None):
        """Saves the sound data to a WAV file."""
        # Write the header.
        chunk_size = 36 + len(sound_data) * self.bytes_per_sample
        if not loop_offset is None:
            if Writer.INCLUDE_LOOP_CUE_CHUNK_IN_WAV:
                chunk_size += 36 # cue_chunk_size
                chunk_size += 29 # list_chunk_size
            if Writer.INCLUDE_LOOP_SMPL_CHUNK_IN_WAV:
                chunk_size += 68 # smpl_chunk_size
        # WAV header.
        file.write("RIFF")
        write_int(file, chunk_size)
        file.write("WAVE")
        file.write("fmt ")
        write_int(file, 16) # subchunk size
        write_short(file, 1) # PCM
        write_short(file, self.channels)
        write_int(file, self.sample_rate)
        write_int(file, self.sample_rate * self.bytes_per_sample * self.channels)
        write_short(file, self.bytes_per_sample * self.channels)
        write_short(file, self.bits_per_sample)
        # data chunk
        file.write("data")
        write_int(file, len(sound_data) * self.bytes_per_sample)
        file.write(struct.pack('h' * len(sound_data), *sound_data))
        if not loop_offset is None:
            # smpl chunk (put first or Goldwave complains about internal chunk size)
            if Writer.INCLUDE_LOOP_SMPL_CHUNK_IN_WAV:
                file.write("smpl")
                write_int(file, 60) # chunk size
                write_int(file, 0) # manufacturer
                write_int(file, 0) # product
                write_int(file, 1000000000 / self.sample_rate); # sample period (samples per nanosecond)
                write_int(file, 60) # MIDI unity note (C5)
                write_int(file, 0) # MIDI pitch fraction
                write_int(file, 0) # SMPTE format
                write_int(file, 0) # SMPTE offset
                write_int(file, 1) # sample loops
                write_int(file, 0) # sampler data
                write_int(file, 0) # cue point ID
                write_int(file, 0) # type (loop forward)
                write_int(file, loop_offset); # start sample number
                write_int(file, len(sound_data) / self.channels) # end sample number
                write_int(file, 0) # fraction
                write_int(file, 0) # playcount
            if Writer.INCLUDE_LOOP_CUE_CHUNK_IN_WAV:
                # cue chunk
                file.write("cue ")
                write_int(file, 4 + 1 * 24) # chunk data size
                write_int(file, 1) # number of cue points
                write_int(file, 0) # ID
                write_int(file, loop_offset) # play order position
                file.write("data") # data chunk id
                write_int(file, 0) # chunk start
                write_int(file, 0) # block start
                write_int(file, loop_offset) # sample offset
                # list chunk, for cue label
                file.write("LIST") # Goldwave only recognizes uppercase
                write_int(file, 21) # 4 + 4 + 4 + 4 + 5
                file.write("adtl")
                file.write("labl")
                write_int(file, 4 + 5) # "loop" + NUL
                write_int(file, 0) # cue point id
                file.write("loop" + "\0")
