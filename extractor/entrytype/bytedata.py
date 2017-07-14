from . import AbstractEntry

class ByteData(AbstractEntry):
    """This class is just a byte array read directly from the ROM."""
    _data = None
    _length = None

    def __init__(self, offset, name, length):
        AbstractEntry.__init__(self, offset, name)
        self._length = length

    def load(self, rom):
        rom.seek(self.offset)
        self._data = rom.read(length)

    def save(self, path, filename=None, filetype=None):
        filename = self._get_filename(path, filename, '{}_0x{:x}.bin'.format(self.name, self.offset))
        with open(filename, 'wb') as f:
            f.write(self._data)

    def _get_length(self):
        return self._length
