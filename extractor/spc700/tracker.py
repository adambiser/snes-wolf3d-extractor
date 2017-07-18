from ..utils import *
from ..wav import wav

class Tracker:
    """A simple monoaural tracker for exporting Wolfenstein 3D songs to WAV.

    Note: This does not emulate the SPC700 exactly.
    It uses linear interpolation for resampling.
    """
    VOICE_COUNT = 8
    SAMPLE_RATE = 32000
    
    def __init__(self, instrument_list, sample_rate=SAMPLE_RATE):
        self.instrument_list = instrument_list
        self.sample_rate = sample_rate

    def write(self, file, song_data):
        """Saves the song data to a WAV file."""
        # Convert song data to wav.
        data = self.convert_to_wav(song_data)
        # Save wav data.
        w = wav.Writer(self.sample_rate, 1, 16)
        w.write(file, data)

    @staticmethod
    def get_total_ticks(events):
        return sum([event.ticks for event in events[1:]])

    def convert_to_wav(self, events):
        """Converts the song data to wav data."""
        # Calculate total song length now for faster processing.
        total_ticks = Tracker.get_total_ticks(events)
##        skip_ticks = 25 * 60
##        total_ticks -= skip_ticks
        voices = [_Voice(self.sample_rate, total_ticks) for v in range(Tracker.VOICE_COUNT)]
        ticks = 0
        # Start at 1 to skip past the instrument list at the beginning.
        for event in events[1:]:
            # Process ticks
            if ticks > 0:
##                if skip_ticks > 0:
##                    skip_ticks -= ticks
##                else:
                for v in voices:
                    v.process_ticks(ticks)
##                voices[0].process_ticks(ticks)
                ticks = 0
            # Process event.
            ticks = event.ticks
            voice = voices[event.voice]
            if event.command == Event.NOTE_ON:
                if voice.instrument.is_percussion:
                    voice.do_note_on(velocity=event.args[0])
                else:
                    voice.do_note_on(*event.args)
            elif event.command == Event.NOTE_OFF:
                voice.do_note_off()
            elif event.command == Event.PITCH_BEND:
                voice.do_pitch_bend(event.args[0])
            elif event.command == Event.CHANGE_INSTRUMENT:
                voice.change_instrument(self.instrument_list[event.args[0]])
            elif event.command == Event.END_SONG:
                break
            elif event.command == Event.PERCUSSION_NOTE_ON:
                voice.do_percussion_note_on()
        # Mix voices.
        output = voices[0].get_audio_data()
        for v in range(1, len(voices)):
            vdata = voices[v].get_audio_data()
            output = [output[x] + vdata[x] for x in range(len(output))]
        return [wav.clamp_short(x) for x in output]

class Event:
    """An event in the tracker song."""
    # Command constants
    NOTE_ON = 1
    NOTE_OFF = 2
    PITCH_BEND = 3
    CHANGE_INSTRUMENT = 4
    END_SONG = 5
    PERCUSSION_NOTE_ON = 6

    def __init__(self, command=None, voice=None, ticks=None, args=None):
        self.command = command
        self.voice = voice
        self.ticks = ticks # Ticks AFTER the event.
        self.args = args

    @classmethod
    def from_byte(cls, code):
        return Event((code >> 5) & 7, (code >> 2) & 7, code & 3)

    @staticmethod
    def get_command_name(code):
        return ['Note On', 'Note Off', 'Pitch Bend', 'Change Instrument', 'End Song', 'Percussion Note On'][code - 1] if 1 <= code <= 6 else 'UNKNOWN'

    def __str__(self):
        return 'Voice {}, Ticks {}, Command: {}, args {}'.format(self.voice, self.ticks, Event.get_command_name(self.command), self.args)

class _Voice:
    """Represents a voice on the SPC700."""
    _PITCH_BEND_CENTER = 0x80 # 0x80 means no pitch bend.
    TICKS_PER_SECOND = 60
    _COUNT = 0
    # Note states
    ATTACK = 0
    DECAY = 1
    SUSTAIN = 2
    RELEASE = 3
    RATE_TABLE = [ None, 0x800, 0x600, 0x500, 0x400, 0x300, 0x280, 0x200,
                   0x180, 0x140, 0x100, 0xc0, 0xa0, 0x80, 0x60, 0x50,
                   0x40, 0x30, 0x28, 0x20, 0x18, 0x14, 0x10, 0xc,
                   0xa, 0x8, 0x6, 0x5, 0x4, 0x3, 0x2, 0x1]

    def __init__(self, sample_rate, total_ticks):
        _Voice._COUNT += 1
        self._voice_number = _Voice._COUNT
        self.samples_per_tick_output = sample_rate / _Voice.TICKS_PER_SECOND
        self.output = [0] * total_ticks * self.samples_per_tick_output
        self.output_pos = 0
        # Current voice settings.
        self.instrument = None
        self.fade_buffer = None
        self.active = False
        self.pitch = None
        self.pitch_bend = 0
        self.velocity = None
        self.buffer_pos = 0
        self.tested = 0
        self.env_state = None
        self.env_counter = 0
        self.envelope = 0
        self.env_vol = 0
        # These values are from SPC dumps using snes9x. They never seem to change.
        self.adsr0 = 0xfe
        self.adsr1 = 0xe9

    def get_audio_data(self):
        return self.output

    def do_note_on(self, note_number=None, velocity=None):
        self.active = True
        self.env_state = _Voice.ATTACK
        self.env_counter = 1
        if not note_number is None:
            self.pitch = self.instrument.pitch[note_number]
        if not velocity is None:
            self.velocity = self.velocity_table[velocity]
        self.buffer_pos = 0

    def do_note_off(self):
        self.active = False
        self.env_state = _Voice.RELEASE
        self.pitch_bend = 0
        # Fade note to 0 so there's no clicking.
        if not self.instrument is None:
            sample_count = 50
            fade_buffer = [0] * sample_count
            self.write_samples(fade_buffer, 0, sample_count)
            fade_buffer = [int(fade_buffer[x] * ((sample_count - x) / float(sample_count))) for x in range(sample_count)]
            for x in range(1, sample_count):
                if (fade_buffer[x] == 0) or ((fade_buffer[x - 1] < 0) != (fade_buffer[x] < 0)):
                    fade_buffer = fade_buffer[:x]
                    break
            self.fade_buffer = fade_buffer

    def do_pitch_bend(self, amount):
        self.pitch_bend = int(self.pitch * (-(0x80 - amount) / 1024.0))

    def change_instrument(self, instrument):
        self.do_note_off()
        self.instrument = instrument
        self.sound_data = instrument.data
        self.loop_offset = instrument.loop_offset
        self.velocity_table = instrument.velocity
        # Percussion instruments only have one pitch value. Set it here.
        if instrument.is_percussion:
            self.pitch = instrument.pitch

    def do_percussion_note_on(self):
        self.do_note_on()

    def process_ticks(self, ticks):
        """Process the given number of ticks based upon the current voice settings."""
        sample_count = self.samples_per_tick_output * ticks
        if self.active:
            output_pos = self.output_pos
            self.write_samples(self.output, output_pos, sample_count)
        # Process any fade buffer caused by a note off.
        if not self.fade_buffer is None:
            output_pos = self.output_pos
            for s in range(len(self.fade_buffer)):
                self.output[output_pos + s] += self.fade_buffer[s]
            self.fade_buffer = None
        self.output_pos += sample_count

    def write_samples(self, output, output_pos, sample_count):
        # Use local variables for faster processing.
        # Pitch is a 14-bit value. The data has 0x52c2 for one instrument, but this is really 0x12c2.
        sample_step = ((self.pitch & 0x3fff) + self.pitch_bend) / 4096.0
        buffer_pos = self.buffer_pos
        inst_data = self.sound_data
        inst_data_len = len(inst_data)
        loop_offset = self.loop_offset
        volume = self.velocity / 20.0
        # Now step through the samples.
        for s in range(sample_count):
            if buffer_pos >= inst_data_len:
                if loop_offset is None:
                    self.active = False
                    break
                else:
                    buffer_pos = loop_offset + buffer_pos % 1
            # Linear interpolation to smoothen the sound.
            interp_pos = buffer_pos % 1
            int_buffer_pos = int(buffer_pos)
            sample = inst_data[int_buffer_pos] * (1 - interp_pos)
            if buffer_pos + 1 < inst_data_len:
                sample += inst_data[int_buffer_pos + 1] * (interp_pos)
            elif not loop_offset is None:
                sample += inst_data[loop_offset] * (interp_pos)
            self.env_counter -= 1
            if self.env_counter <= 0:
                self.do_envelope()
            output[output_pos + s] = int(sample * volume * self.env_vol)
            buffer_pos += sample_step
        self.buffer_pos = buffer_pos

    def do_envelope(self):
        # Based on https://github.com/snes9xgit/snes9x/blob/master/apu/bapu/dsp/SPC_DSP.cpp#L206
        # The rate table used by here is the inverse.
        envelope = self.envelope
        if self.env_state == _Voice.RELEASE:
            rate = 1
            envelope -= 8
            if envelope < 0:
                envelope = 0
                self.active = False
        else:
            # Always ADSR mode, not GAIN.
            env_data = self.adsr1
            if self.env_state >= _Voice.DECAY:
                envelope -= 1
                envelope -= (envelope >> 8)
                rate = self.adsr1 & 0x1f
                if self.env_state == _Voice.DECAY:
                    rate = (self.adsr0 >> 3 & 0xe) + 0x10
            else: # ATTACK
                rate = (self.adsr0 & 0x0f) * 2 + 1
                envelope += 0x20 if rate < 31 else 0x400
            if ((envelope >> 8) == (env_data >> 5)) and (self.env_state == _Voice.DECAY):
		self.env_state = _Voice.SUSTAIN
	    if envelope > 0x7ff or envelope < 0:
                envelope = 0 if envelope < 0 else 0x7ff
                if self.env_state == _Voice.ATTACK:
                    self.env_state = _Voice.DECAY
        self.envelope = envelope
        self.env_vol = envelope / float(0x7ff)
        self.env_counter = _Voice.RATE_TABLE[rate]
##        print '{} State {} - {}, {}, {}'.format(self._voice_number, self.env_state, self.envelope, self.env_vol, self.env_counter)
