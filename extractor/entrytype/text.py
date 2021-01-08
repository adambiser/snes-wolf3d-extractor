import re

from .bytedata import ByteData


class Text(ByteData):
    """An entry with simple ASCII text."""

    def __init__(self, offset, length, name, linesplit='\x00', has_length_byte=False):
        super().__init__(offset, length, name)
        self.linesplit = linesplit
        self.has_length_byte = has_length_byte
        self._data = None
        
    def load(self, rom):
        data = rom.read_text_chunk(self.offset, self._length)
        if self.has_length_byte:
            self._data = ''
            while data:
                if self._data:
                    self._data += '\n'
                split = ord(data[0]) + 1
                self._data += data[1:split]
                data = data[split:]
        else:
            self._data = '\n'.join(re.split(self.linesplit, data))

    def save(self, path, filename=None, filetype=None):
        filename = self._get_filename(path, filename, self.name + '.txt')
        with open(filename, 'w') as f:
            f.write(self._data)
