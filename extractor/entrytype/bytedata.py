from .abstractentry import AbstractEntry


class ByteData(AbstractEntry):
    """This class is just a byte array read directly from the ROM."""

    def __init__(self, offset: int, length: int, name='unknown'):
        super().__init__(offset, name)
        self._length = length
        self._data = None

    def load(self, rom):
        rom.seek(self.offset)
        self._data = rom.read(self._length)

    def save(self, path, filename=None, filetype=None):
        filename = self._get_filename(path, filename, f'{self.name}_0x{self.offset:x}.bin')
        with open(filename, 'wb') as f:
            f.write(self._data)

    def _get_length(self):
        return self._length
