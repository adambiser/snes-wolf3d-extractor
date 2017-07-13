from abc import ABCMeta, abstractmethod

class Entry:
    __metaclass__ = ABCMeta
    name = None
    offset = None

    '''
    Constructor.
    Store entry name and offset.
    '''
    def __init__(self, rom, name):
        self.name = name
        self.offset = rom.tell()

    '''
    Saves the entry to a filename.
    '''
    @abstractmethod
    def save(self, filename):
        pass

    '''
    Saves the entry to a filename.
    '''
    @abstractmethod
    def save(self, filename):
        pass

    '''
    Returns the default filename for use when saving.
    '''
    def get_default_filename(self):
        return self.name + self.get_default_extension()
