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

# Note elements

from elf.core.property import VALUE_FIXED
from elf.core.header import Header
from elf.core.chunk import Chunk
from struct import calcsize

nhdr_core_type = {
    'NT_PRSTATUS'   : 1,
    'NT_FPREGSET'   : 2,
    'NT_PRPSINFO'   : 3,
    'NT_PRXREG'     : 4,
    'NT_TASKSTRUCT' : 4,
    'NT_PLATFORM'   : 5,
    'NT_AUXV'       : 6,
    'NT_GWINDOWS'   : 7,
    'NT_ASRS'       : 8,
    'NT_PSTATUS'    : 10,
    'NT_PSINFO'     : 13,
    'NT_PRCRED'     : 14,
    'NT_UTSNAME'    : 15,
    'NT_LWPSTATUS'  : 16,
    'NT_LWPSINFO'   : 17,
    'NT_PRFPXREG'   : 20,
    'NT_PRXFPREG'   : 0x46e62b7f,
    }
for key,value in nhdr_core_type.items(): nhdr_core_type[value] = key

nhdr_type = {
    'NT_VERSION'    : 1,
    }
for key,value in nhdr_type.items(): nhdr_type[value] = key

class NoteHeader( Header ):
    descriptions = [ 'n_namesz', 'n_descz', 'n_type' ]

    format = [ 'I', 'I', 'I' ]

    hr_values = {
        'n_type' : [ VALUE_FIXED, nhdr_type ],
        }

class Note( Chunk ):
    def __init__(self, nhdr):
 
        self.header = nhdr
        self.name = ''
        self.desc = ''

        Chunk.__init__(self, self.header.prop, True, 
                       offset=self.header.offset_start+calcsize(''.join(self.header.format)), 
                       size=self.header.n_namesz+self.header.n_descz)

    def load(self, offset=None, filemap=None):
        Chunk.load(self, offset, filemap)

        self.name = str(self.data[:self.header.n_namesz])
        self.desc = str(self.data[self.header.n_namesz:])

        self.data = None

    def chunks(self):
        return [self, self.header]

#######
# EOF #
#######
