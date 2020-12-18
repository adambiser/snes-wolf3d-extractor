from extractor.entrytype import Map
from extractor.utils import *
import os
import struct
from tempfile import TemporaryFile

def converttobin(f):
    uncompressed_size = read_ushort(f)
    data = [0 for x in range(uncompressed_size)]
    tag = read_ubyte(f)
    match_bits = read_ubyte(f)
    assert match_bits == 4
    index = 0
    while index < len(data):
        b = read_ubyte(f)
        if b == tag:
            b = read_ushort(f)
            count = (b & 0xf) + 3
            offset = (b & 0xfff0) >> 4
            for x in range(0, count):
                data[index] = data[index - offset]
                index += 1
        else:
            data[index] = b
            index += 1
    temp = TemporaryFile()
    temp.write(struct.pack('B' * len(data), *data))
    temp.seek(0)
    return temp

def readbinmap(f, name):
    m = Map(0, name)
    m._walls =  struct.unpack('B' * Map._MAP_SIZE * Map._MAP_SIZE, f.read(Map._MAP_SIZE * Map._MAP_SIZE))
    m._floorcodes =  struct.unpack('B' * 64, f.read(64))
    f.seek(0x100, 1)
    object_count = read_ushort(f)
    object_offset = read_ushort(f)
    f.seek(object_offset)
    m.readobjects(f, object_count)
    return m.generate_dos_map()

def convertbinmaps():
    maps = []
    for x in range(30):
        filename = 'input/TEDSNES/MAP{}.BIN'.format(x)
        print('Loading {}'.format(os.path.basename(filename)))
        with open(filename, 'rb') as f:
            maps.append(readbinmap(f, os.path.basename(filename)))
    Map.save_as_wdc_map_file('SNESBIN.map', maps)

def convertcmpmaps():
    maps = []
    for x in range(30):
        filename = 'input/TEDSNES/MAP{}.CMP'.format(x)
        print('Loading {}'.format(os.path.basename(filename)))
        with open(filename, 'rb') as f:
            m = Map(0, os.path.basename(filename))
            with converttobin(f) as bm:
                maps.append(readbinmap(bm, os.path.basename(filename)))
    Map.save_as_wdc_map_file('SNESCMP.map', maps)

convertbinmaps()
convertcmpmaps()
