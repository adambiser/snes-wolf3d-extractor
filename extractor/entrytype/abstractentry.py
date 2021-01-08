import os
import typing

if typing.TYPE_CHECKING:
    from ..rom import Rom


class AbstractEntry:
    """The base entry class.

    This class defines the generic methods that are available for all entries.
    """

    def __init__(self, offset: int, name: str):
        """Stores the entry offset and name.

        If the offset is -1, the rom will use the previous entry's offset and _get_length() to calculate this entry's
        offset.
        """
        self.offset = offset
        self.name = name

    # TODO Try out this idea.
    def __len__(self):
        raise Exception("Entry does not return a length.")

    def load(self, rom: "Rom"):
        """Loads the entry from the rom.

        :param rom: the rom object containing this entry
        """
        raise NotImplementedError

    def save(self, path: str, filename: str = None, filetype: str = None):
        """Saves the entry to a file.

        :param path: The path to which to save the entry.
        :param filename: If None, the entry's default name is used.
        :param filetype: If None, the entry's default type is used.
        """
        raise NotImplementedError

    def _get_length(self) -> int:
        """Returns the length of the entry within the rom.

        This is only used when adding entries to the rom's entry list that are to start at the offset that immediately
        follows this entry (have -1 as their offset).
        """
        raise Exception("Entry does not return a length.")

    # noinspection PyMethodMayBeStatic
    def _get_filename(self, path: str, given_filename: typing.Optional[str], default_filename: str) -> str:
        return os.path.join(path, given_filename or default_filename)
