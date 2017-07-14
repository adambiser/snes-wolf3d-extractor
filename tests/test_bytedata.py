# Hack so that this test can be run as a main module.
from os import path, sys
sys.path.append(path.dirname(path.dirname(__file__)))

##from extractor.entrytype import AbstractEntry
from extractor.entrytype import *

e = ByteData(0x300, 'name', 123)
e.save("here")
