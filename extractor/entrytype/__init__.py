# Imports from this package need to be after the class definition.
import abc as abc
import os


class AbstractEntry:
    """The base entry class.

    This class defines the generic methods that are available for all entries.
    """
    __metaclass__ = abc.ABCMeta
    name = None
    offset = None

    def __init__(self, offset, name):
        """Stores the entry offset and name.
        
        If the offset is -1, the rom will use the previous entry's
        offset and _get_length() to calculate this entry's offset.
        """
        self.offset = offset
        self.name = name

    @abc.abstractmethod
    def load(self, rom):
        """Loads the entry from the rom.

        args:
            rom - the rom object containing this entry
        """
        pass

    @abc.abstractmethod
    def save(self, path, filename=None, filetype=None):
        """Saves the entry to a file.
        
        args:
            path - The path to which to save the entry.
            filename - If None, the entry's default name is used.
            filetype - If None, the entry's default type is used.
        """
        pass

    def _get_length(self):
        """Returns the length of the entry within the rom.

        This is only used when adding entries to the rom's entry list that
        are to start at the offset that immediately follows this entry
        (have -1 as their offset).
        """
        raise Exception("Entry does not return a length.")

    def _get_filename(self, path, given_filename, default_filename):
        return os.path.join(path, default_filename if given_filename is None else given_filename)


# Import entry types.
from bytedata import ByteData
from image import Image
from instrument_list import InstrumentList
from map import Map
from palette import Palette
from song import Song
from sound import Sound
from sprite import Sprite
from text import Text
