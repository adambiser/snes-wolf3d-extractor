from entry import Entry
from ..utils import *

class Map(Entry):
    # Config settings
    _DETECT_PUSHWALL_DIRECTION_WHEN_CONVERTING_TO_DOS = False
    # Variables
    _walls = None
    _extra = None # The unknown 64 bytes after the end of the wall data.
    _objects = None
    # Constants
    _MAP_SIZE = 64
    _PLANE_COUNT = 2
    _FLOOR_CODE_START = 0x6c
    _FLOOR_CODE_STOP = 0x8f
    _DOOR_CODE_START = 0x5a
    _DOOR_CODE_STOP = 0x61
    _PUSHWALL = 0x62
    # For pushwall direction detection
    _NORTH = 0x1
    _SOUTH = 0x2
    _WEST = 0x4
    _EAST = 0x8

    '''
    Constructor.
    Loads and decompresses the SNES map data from a given file at the current position within the file.
    '''
    def __init__(self, rom, name):
        Entry.__init__(self, rom, name)
        # Assuming this is an uncompressed size, but since this doesn't do anything with the data after the object list, ignore.
        uncompressed_size = read_ushort(rom)
        # This format has 64 extra bytes after the wall data that are compressed the same way.
        self._walls = [0 for x in range(Map._MAP_SIZE * Map._MAP_SIZE + 64)]
        # Decompress the wall data.
        tag = read_ubyte(rom)
        match_bits = read_ubyte(rom)
        assert match_bits == 4
        index = 0
        while index < len(self._walls):
            b = read_ubyte(rom)
            if b == tag:
                b = read_ubyte(rom)
                count = (b & 0xf) + 3
                offset = ((b & 0xf0) >> 4) | (read_ubyte(rom) << 4)
                for x in range(0, count):
                    self._walls[index] = self._walls[index - offset]
                    index += 1
            else:
                self._walls[index] = b
                index += 1
        # Split the extra 64 bytes into a new list and remove them from the wall bytes.
        self._extra = self._walls[-64:]
        self._walls = self._walls[:-64]
        # Read the object list.
##        print 'map offset: {:x}, object start: {:x}'.format(self.offset, rom.tell())
        object_count = read_ushort(rom)
##        print 'object_count: {:x}'.format(object_count)
        rom.seek(0x6, 1)
        self._objects = []
        for o in range(object_count):
            x = rom.read(1)
            if x == '':
                break
            x = struct.unpack('<B', x)[0]
            y = read_ubyte(rom)
##            assert 0 <= x <= Map._MAP_SIZE, 'Object off the map at {}, {}'.format(x, y)
##            assert 0 <= y <= Map._MAP_SIZE, 'Object off the map at {}, {}'.format(x, y)
            # Correct out of bounds objects... TODO why does this happen?
            if x < 0: x += Map._MAP_SIZE
            if x >= Map._MAP_SIZE: x -= Map._MAP_SIZE
            if y < 0: y += Map._MAP_SIZE
            if y >= Map._MAP_SIZE: y -= Map._MAP_SIZE
                
            object_code = read_ubyte(rom)
            self._objects.append({
                'x': x,
                'y': y,
                'code': object_code
                })
            # Pushwalls have an extra byte indicating its wall tile.
            if object_code == Map._PUSHWALL:
                self._objects[-1]['wall'] = read_ubyte(rom)

    '''
    Converts the SNES map data to DOS map format.
    Returns the map as plane data.
    Note that this is not perfect because of how pushwalls work in the SNES.
    When _DETECT_PUSHWALL_DIRECTION_WHEN_CONVERTING_TO_DOS is True, it does its best to convert SNES pushwalls to DOS pushwalls.
    '''
    def generate_dos_map(self):
        # Convert wall code
        tiles = [[0 for x in range(len(self._walls))] for p in range(Map._PLANE_COUNT)]
        for index in range(0, len(self._walls)):
            tiles[0][index] = self._walls[index]
            if tiles[0][index] >= 0x80:
                tiles[0][index] -= 0x80
            else:
                tiles[0][index] += Map._FLOOR_CODE_START
        # Place objects.
        for obj in self._objects:
            index = obj['x'] + obj['y'] * Map._MAP_SIZE
            # Doors are stored in the object plane. The wall plane has a floor code for these tiles.
            # Place doors in the wall plane instead.
            if Map._DOOR_CODE_START <= obj['code'] <= Map._DOOR_CODE_STOP:
                tiles[0][index] = obj['code']
            else:
                tiles[1][index] = obj['code']
                # Pushwalls have an extra byte indicating the wall tile. The wall plane has a floor code.
                # Place the wall tile in the wall plane for DOS maps.
                if obj['code'] == Map._PUSHWALL:
                    self._fix_pushwall(tiles, obj)
        return {
            'name': self.name,
            'tiles': tiles,
            }

    '''
    Converts the SNES pushwalls into tiles that DOS pushwalls need to work.
    The SNES pushwall went into a wall in its final step. DOS pushwalls need all times to be floor codes.
    When _DETECT_PUSHWALL_DIRECTION_WHEN_CONVERTING_TO_DOS is True, this attempts to determine the pushwall
    direction and converts the end tile to a floor code so that would work in the DOS game.
    '''
    def _fix_pushwall(self, tiles, obj):
        index = obj['x'] + obj['y'] * Map._MAP_SIZE
        tiles[0][index] = obj['wall']
        if not self._DETECT_PUSHWALL_DIRECTION_WHEN_CONVERTING_TO_DOS:
            return
        # On the SNES, pushwalls act like objects that move into a wall at its final position.
        # Check each direction to see if it's a possible move.
        move_dir = 0
        if self._is_pushwall_direction(tiles, obj, 'y', -1):
            move_dir |= Map._NORTH
        if self._is_pushwall_direction(tiles, obj, 'y', 1):
            move_dir |= Map._SOUTH
        if self._is_pushwall_direction(tiles, obj, 'x', -1):
            move_dir |= Map._WEST
        if self._is_pushwall_direction(tiles, obj, 'x', 1):
            move_dir |= Map._EAST
        # If there's only one possible move direction, set the end tile to be the floor code.
        if move_dir == Map._NORTH:
            tiles[0][index - Map._MAP_SIZE * 2] = tiles[0][index - Map._MAP_SIZE]
        elif move_dir == Map._SOUTH:
            tiles[0][index + Map._MAP_SIZE * 2] = tiles[0][index + Map._MAP_SIZE]
        elif move_dir == Map._WEST:
            tiles[0][index - 2] = tiles[0][index - 1]
        elif move_dir == Map._EAST:
            tiles[0][index + 2] = tiles[0][index + 1]
        else:
            # Did not find one and only one direction. Report it.
            dirs = []
            if move_dir == 0:
                dirs.append("none")
            else:
                if move_dir & Map._NORTH:
                    dirs.append("north")
                if move_dir & Map._SOUTH:
                    dirs.append("south")
                if move_dir & Map._WEST:
                    dirs.append("west")
                if move_dir & Map._EAST:
                    dirs.append("east")
            print 'Could not determine direction for pushwall at {},{}, choices: {}'.format(obj['x'], obj['y'], ', '.join(dirs))

    '''
    Checks to see whether a direction is a valid move for a pushwall.
    '''
    def _is_pushwall_direction(self, tiles, obj, move_coord_name, move_step):
        other_coord_name = 'x' if move_coord_name == 'y' else 'y'
        steps = [{
            move_coord_name: obj[move_coord_name] + (x + 1) * move_step,
            other_coord_name: obj[other_coord_name]
            } for x in range(2)]
        # Bounds check.
        if not (1 <= steps[1][move_coord_name] < Map._MAP_SIZE - 1):
            return False
        # Make sure the first step is a floor code.
        if not Map._is_dos_floor_code(tiles[0][steps[0]['x'] + steps[0]['y'] * Map._MAP_SIZE]):
            return False
        # See if the last step is a wall that matches the pushwall wall code.
        return tiles[0][steps[1]['x'] + steps[1]['y'] * Map._MAP_SIZE] == obj['wall']

    '''
    Tests to see if a code is a valid DOS map floor code.
    '''
    @staticmethod
    def _is_dos_floor_code(code):
        return Map._FLOOR_CODE_START <= code <= Map._FLOOR_CODE_STOP

    '''
    Saves the given maps to a WDC map file.
    This assumes that the given maps are in the DOS map format.
    '''
    @staticmethod
    def save_as_wdc_map_file(filename, maps):
        print "Saving %d maps to %s" % (len(maps), filename)
        with open(filename, 'wb') as f:
            f.write('WDC3.1')
            write_int(f, len(maps))
            write_short(f, Map._PLANE_COUNT)
            write_short(f, 16) # map name length
            for m in maps:
                f.write(m['name'] + '\00' * (16 - len(m['name'])))
                write_short(f, Map._MAP_SIZE)
                write_short(f, Map._MAP_SIZE)
                for p in range(Map._PLANE_COUNT):
                    f.write(struct.pack('<{}H'.format(len(m['tiles'][p])), *m['tiles'][p]))

    '''
    Saves this map to a WDC map file.
    This assumes that the given maps are in the SNES map format.
    '''
    def save(self, filename):
        Map.save_as_wdc_map_file(filename, [self.generate_dos_map()])

    '''
    Returns the default file extension to use while saving.
    Should be with the period.
    '''
    def get_default_extension(self):
        return ".map"
