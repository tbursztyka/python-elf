"""
  Copyright (C) 2008-2011  Tomasz Bursztyka

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

# Relocation elements  

from elf.core.property import ARCH_32, ARCH_64
from elf.core.header import Header

class RelocationEntry( Header ):
    descriptions = [ 'r_offset', 'r_info' ]

    format_32 = [ 'I', 'i' ]
    format_64 = [ 'Q', 'q' ]

    def __init__(self, prop, offset=None):
        Header.__init__(self, prop, offset)

        self.r_sym = self.getSym()
        self.r_type = self.getType()

    def getSym(self):
        if self.prop.arch == ARCH_32:
            return (self.r_info >> 8)
        elif self.prop.arch == ARCH_64:
            return (self.r_info >> 32)
        else:
            return 0

    def getType(self):
        if self.prop.arch == ARCH_32:
            return (self.r_info & 0xff)
        elif self.prop.arch == ARCH_64:
            return (self.r_info & 0xffffffff)
        else:
            return 0

class RelocationAEntry( RelocationEntry ):
    descriptions = [ 'r_offset', 'r_info', 'r_addend' ]

    format_32 = [ 'I', 'i', 'i' ]
    format_64 = [ 'Q', 'q', 'q' ]

#######
# EOF #
#######

