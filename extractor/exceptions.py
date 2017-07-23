class RomInfoNotFoundError(Exception):
    """The error raised when ROM info is not found for the given CRC32."""
    def __init__(self, crc32, *args):
        super(RomInfoNotFoundError, self).__init__(crc32, *args)
        self.crc32 = crc32
