from . import AbstractEntry
from .. import utils
import struct

class Map(AbstractEntry):
    """Reads a Wolfenstein 3D map stored in the SNES format.

    Can convert to the DOS format and save to the WDC file format.
    """
    # Config settings
    DETECT_PUSHWALL_DIRECTION_WHEN_CONVERTING_TO_DOS = False
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

    def __init__(self, offset, name):
        AbstractEntry.__init__(self, offset, name)

    def load(self, rom):
        rom.seek(self.offset)
        # Assuming this is an uncompressed size, but since this code doesn't do
        # anything with the data after the object list, ignore.
        uncompressed_size = rom.read_ushort()
        # This format has 64 extra bytes after the wall data that are compressed the same way.
        self._walls = [0 for x in range(Map._MAP_SIZE * Map._MAP_SIZE + 64)]
        # Read and decompress the wall data.
        tag = rom.read_ubyte()
        # Number of bits for the value of 'count' down below.
        match_bits = rom.read_ubyte()
        assert match_bits == 4
        index = 0
        while index < len(self._walls):
            b = rom.read_ubyte()
            if b == tag:
                b = rom.read_ushort()
                count = (b & 0xf) + 3
                offset = (b & 0xfff0) >> 4
                for x in range(0, count):
                    self._walls[index] = self._walls[index - offset]
                    index += 1
            else:
                self._walls[index] = b
                index += 1
        # Split the extra 64 bytes into a new list and remove them from the wall bytes.
        self._extra_bytes = self._walls[-64:]
        self._walls = self._walls[:-64]
        # Read the object list.
        object_count = rom.read_ushort()
        rom.seek(0x6, 1)
        self._objects = []
        for o in range(object_count):
            x = rom.read(1)
            if x == '':
                break
            x = struct.unpack('<B', x)[0]
            y = rom.read_ubyte()
##            assert 0 <= x <= Map._MAP_SIZE, 'Object off the map at {}, {}'.format(x, y)
##            assert 0 <= y <= Map._MAP_SIZE, 'Object off the map at {}, {}'.format(x, y)
            if not (0 <= x <= Map._MAP_SIZE and 0 <= y <= Map._MAP_SIZE):
                print '{} had an object located off the map at {}, {}. Correcting.'.format(self.name, x, y)
            # Correct out of bounds objects... TODO why does this happen?
            if x < 0: x += Map._MAP_SIZE
            if x >= Map._MAP_SIZE: x -= Map._MAP_SIZE
            if y < 0: y += Map._MAP_SIZE
            if y >= Map._MAP_SIZE: y -= Map._MAP_SIZE
            object_code = rom.read_ubyte()
            self._objects.append({
                'x': x,
                'y': y,
                'code': object_code
                })
            # Pushwalls have an extra byte indicating its wall tile.
            if object_code == Map._PUSHWALL:
                self._objects[-1]['wall'] = rom.read_ubyte()

    def generate_dos_map(self):
        """Converts the SNES map data to DOS map format.

        This is not perfect because of how pushwalls work in the SNES.
        See _fix_pushwall() for further information.

        Returns a dict with the map's name in 'name' and plane data in 'tiles'.
        """
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
                    Map._fix_pushwall(tiles, obj)
        return {
            'name': self.name,
            'tiles': tiles,
            }

    @staticmethod
    def _fix_pushwall(tiles, obj):
        """Converts the SNES pushwalls into tiles that DOS pushwalls need to work.

        SNES pushwalls are objects with a wall code that moves two spaces and go
        into a wall in its final resting spot.

        DOS pushwalls are moving walls and move two spots or until they hit a
        wall.

        This code places a pushwall's wall code into the wall plane and
        when DETECT_PUSHWALL_DIRECTION_WHEN_CONVERTING_TO_DOS is True,
        this attempts to find the direction the pushwall is supposed to move
        and sets that wall tile to the appropriate floor code.
        """
        index = obj['x'] + obj['y'] * Map._MAP_SIZE
        tiles[0][index] = obj['wall']
        if not Map.DETECT_PUSHWALL_DIRECTION_WHEN_CONVERTING_TO_DOS:
            return
        # Check each direction to find all valid moves.
        move_dir = 0
        if Map._is_valid_pushwall_direction(tiles, obj, 'y', -1):
            move_dir |= Map._NORTH
        if Map._is_valid_pushwall_direction(tiles, obj, 'y', 1):
            move_dir |= Map._SOUTH
        if Map._is_valid_pushwall_direction(tiles, obj, 'x', -1):
            move_dir |= Map._WEST
        if Map._is_valid_pushwall_direction(tiles, obj, 'x', 1):
            move_dir |= Map._EAST
        # If there's only one valid move direction, set the end tile to be the floor code.
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

    @staticmethod
    def _is_valid_pushwall_direction(tiles, obj, move_coord_name, move_step):
        """Returns true if direction is a valid move for a pushwall."""
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

    @staticmethod
    def _is_dos_floor_code(code):
        """Returns True when code is a valid DOS map floor code."""
        return Map._FLOOR_CODE_START <= code <= Map._FLOOR_CODE_STOP

    @staticmethod
    def save_as_wdc_map_file(filename, maps):
        """Saves all given maps to a single WDC map file

        This assumes that the given maps are in the DOS map format.
        """
        print "Saving %d maps to %s" % (len(maps), filename)
        with open(filename, 'wb') as f:
            f.write('WDC3.1')
            utils.write_int(f, len(maps))
            utils.write_short(f, Map._PLANE_COUNT)
            utils.write_short(f, 16) # map name length
            for m in maps:
                f.write(m['name'] + '\00' * (16 - len(m['name'])))
                utils.write_short(f, Map._MAP_SIZE)
                utils.write_short(f, Map._MAP_SIZE)
                for p in range(Map._PLANE_COUNT):
                    f.write(struct.pack('<{}H'.format(len(m['tiles'][p])), *m['tiles'][p]))

    def save(self, path, filename=None, filetype=None):
        """Saves the map to a WDC map file."""
        filename = self._get_filename(path, filename, self.name + '.map')
        Map.save_as_wdc_map_file(filename, [self.generate_dos_map()])
