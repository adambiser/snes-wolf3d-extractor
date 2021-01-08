import errno
import os
import struct


def read_ubyte(f) -> int:
    """Reads an unsigned byte."""
    return struct.unpack('<B', f.read(1))[0]


def read_ushort(f) -> int:
    """Reads an unsigned short."""
    return struct.unpack('<H', f.read(2))[0]


def signed_nibble(x) -> int:
    """Converts an unsigned nibble to a signed nibble."""
    return (x | ~7) if (x & 8) else (x & 7)


def write_short(f, x: int):
    """Writes a signed short"""
    f.write(struct.pack('<h', x))


def write_int(f, x: int):
    """Writes a signed integer."""
    f.write(struct.pack('<i', x))


def create_path(path: str):
    """Creates the given path and ignores the error raised if the path already exists."""
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def insert_string(string: str, index: int, insert: str):
    """Inserts a string at a given index within another strings."""
    return string[:index] + insert + string[index:]
