from entry import Entry

'''
This class is basically just a byte array of unknown meaning from the ROM.
'''
class ByteData(Entry):
    _data = None

    '''
    Constructor.
    Loads byte data from the current postiion within the rom.
    '''
    def __init__(self, rom, name, length):
        Entry.__init__(self, rom, name)
        self._name += '_' + hex(self.offset)
        self._data = rom.read(length)

    '''
    Gets the data length.
    '''
    @staticmethod
    def get_data_length(length):
        return length


    '''
    Saves the given byte data to the given filename.
    '''
    def save(self, filename):
        with open(filename, 'wb') as f:
            f.write(self._data)

    '''
    Returns the default file extension to use while saving.
    Should begin with the period.
    '''
    def get_default_filename(self):
##        return self._name + '_' + hex(self.offset) + '.bin'
        return self._name + '.bin'
