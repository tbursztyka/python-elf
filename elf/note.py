"""
  Copyright (C) 2008-2013  Tomasz Bursztyka

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published
  by the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

""" NoteHeader and Note classes """

from elf.core.property import VALUE_FIXED
from elf.core.header import Header
from elf.core.page import Page
from elf.utils import mirrorDict
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
nhdr_core_type = mirrorDict(nhdr_core_type)

nhdr_type = {
    'NT_VERSION'    : 1,
    }
nhdr_type = mirrorDict(nhdr_type)


class NoteHeader( Header ):
    descriptions = [ 'n_namesz', 'n_descz', 'n_type' ]

    format = [ 'I', 'I', 'I' ]

    hr_values = {
        'n_type' : [ VALUE_FIXED, nhdr_type ],
        }

class Note( Page ):
    def __init__(self, nhdr):
        self.name = ''
        self.desc = ''

        Page.__init__(self, nhdr,
                      nhdr.offset_start+calcsize(''.join(nhdr.format)),
                      nhdr.n_namesz+nhdr.n_descz)

    def load(self, offset=None, filemap=None):
        Page.load(self, offset, filemap)

        self.name = str(self.data[:self.header.n_namesz])
        self.desc = str(self.data[self.header.n_namesz:])

#######
# EOF #
#######
