from .abstractentry import AbstractEntry
from .instrument_list import InstrumentList
from ..spc700.tracker import Event
from ..spc700.tracker import Tracker


class Song(AbstractEntry):
    """Represents a song.

    When loaded, the entry consists of an array of Tracker.Event objects which can be passed to the tracker to write
    a WAV.
    """

    def __init__(self, offset, name):
        super().__init__(offset, name)
        self._instruments = None
        self.events = None

    def load(self, rom):
        self._instruments = rom.get_entry(rom.get_entries_of_class(InstrumentList)[0])
        rom.seek(self.offset)
        # Load song into an array of song events.
        # First entry is a pseudo-event for instrument numbers.
        events = [Event(args=[rom.read_ubyte()])]
        # Instrument numbers (corresponds to MIDI instruments).
        events[-1].args.extend(rom.read_ubyte() for _ in range(events[-1].args[0]))
        # Read song data.
        while True:
            event = Event.from_byte(rom.read_ubyte())
            events.append(event)
            # If ticks = 3, the next byte holds the actual value.
            if event.ticks == 3:
                event.ticks = rom.read_ubyte()
                # If it's 0 now, set it to 256.
                if event.ticks == 0:
                    event.ticks = 256
            # Read byte args for command.
            if event.command == Event.NOTE_ON:
                # Note number for melodic instruments.
                # Velocity for percussion instruments.
                event.args = [rom.read_ubyte()]
                # This flag means the next byte is velocity for melodic instruments only.
                # Since velocity is 0..127, percussion instruments should never have this flag set.
                if event.args[-1] & 0x80:
                    event.args[-1] &= 0x7f
                    event.args += [rom.read_ubyte()]
            elif event.command == Event.NOTE_OFF:
                pass
            elif event.command == Event.PITCH_BEND:
                # Pitch bend amount.
                event.args = [rom.read_ubyte()]
            elif event.command == Event.CHANGE_INSTRUMENT:
                # Instrument number.
                event.args = [rom.read_ubyte()]
            elif event.command == Event.END_SONG:
                break
            elif event.command == Event.PERCUSSION_NOTE_ON:
                pass
            # print event
        self.events = events

    def save(self, path, filename=None, filetype=None):
        """Saves the song as a WAV file."""
        filename = self._get_filename(path, filename, self.name + '.wav')
        with open(filename, 'wb') as f:
            t = Tracker(self._instruments)
            t.write(f, self.events)
