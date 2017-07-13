import errno
import os
import struct

'''
Reads an unsigned byte from a file.
'''
def read_ubyte(f):
    return struct.unpack('<B', f.read(1))[0]

'''
Reads an unsigned short from a file.
'''
def read_ushort(f):
    return struct.unpack('<H', f.read(2))[0]

'''
Converts an unsigned nibble to a signed nibble.
'''
def signed_nibble(x):
    return (x | ~7) if (x & 8) else (x & 7)

'''
Writes a signed short to a file.
'''
def write_short(f, x):
    f.write(struct.pack('<h', x))

'''
Writes a signed integer to a file.
'''
def write_int(f, x):
    f.write(struct.pack('<i', x))

'''
Creates the given path and ignores the error raised if the path already exists.
'''
def create_path(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
'''
Inserts a string at a given index within another strings.
'''
def insert_string(string, index, insert_string):
    return string[:index] + insert_string + string[index:]
