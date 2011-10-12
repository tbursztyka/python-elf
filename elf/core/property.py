"""
  Copyright (C) 2008-2011  See AUTHORS

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

""" Property type """

from struct import pack, calcsize
from mmap import ACCESS_READ

LITTLE_ENDIAN = '<'
BIG_ENDIAN = '>'

ARCH_32 = 32
ARCH_64 = 64

VALUE_FIXED = 1 << 0
VALUE_BITWISE = 1 << 1

class Property:
    """ Basic properties for elf module """
    def __init__(self, mode=None, backup=False, filename=None, size_src=None):
        """ Constructor """
        self.mode = mode
        if self.mode == None:
            self.mode = ACCESS_READ

        self.backup = backup
        self.filename = filename
        self.size_src = size_src

        self.size_dst = None
        self.file_src = None
        self.file_dst = None
        self.map_src = None
        self.map_dst = None
        self.arch = None
        self.endian = None

        native = pack('@h', 1)
        little = pack('<h', 1)

        if native == little:
            self.endian = LITTLE_ENDIAN
        else:
            self.endian = BIG_ENDIAN

        if calcsize("P") == 8:
            self.arch = ARCH_64
        else:
            self.arch = ARCH_32

#######
# EOF #
#######

