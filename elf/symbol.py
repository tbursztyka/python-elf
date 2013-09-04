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

""" SymbolTableEntry and SymbolInfo classes """

from elf.core.property import ARCH_32, ARCH_64, VALUE_FIXED, VALUE_BITWISE
from elf.core.header import Header
from elf.utils import mirrorDict

symtab_bind = {
    'STB_LOCAL'             : 0,
    'STB_GLOBAL'            : 1,
    'STB_WEAK'              : 2,
    'STB_NUM'               : 3,
    'STB_LOOS'              : 10,
    'STB_HIOS'              : 12,
    'STB_LOPROC'            : 13,
    'STB_HIPROC'            : 15,
    'STB_MIPS_SPLIT_COMMON' : 13,
    }
mirrorDict(symtab_bind)

symtab_type = {
    'STT_NOTYPE'           : 0,
    'STT_OBJECT'           : 1,
    'STT_FUNC'             : 2,
    'STT_SECTION'          : 3,
    'STT_FILE'             : 4,
    'STT_COMMON'           : 5,
    'STT_TLS'              : 6,
    'STT_NUM'              : 7,
    'STT_LOOS'             : 10,
    'STT_HIOS'             : 12,
    'STT_LOPROC'           : 13,
    'STT_HIPROC'           : 15,
    'STT_SPARC_REGISTER'   : 13,
    'STT_PARISC_MILLICODE' : 13,
    'STT_HP_OPAQUE'        : (10 + 0x1),
    'STT_HP_STUB'          : (10 + 0x2),
    'STT_ARM_TFUNC'        : 0xd,
    }
mirrorDict(symtab_type)

symtab_visibility = {
    'STV_DEFAULT'   : 0,
    'STV_INTERNAL'  : 1,
    'STV_HIDDEN'    : 2,
    'STV_PROTECTED' : 3,
    }
mirrorDict(symtab_visibility)

syminfo_boundto = {
    'SYMINFO_BT_SELF'       : 0xffff,
    'SYMINFO_BT_PARENT'     : 0xfffe,
    'SYMINFO_BT_LOWRESERVE' : 0xff00,
    }
mirrorDict(syminfo_boundto)

syminfo_flags = {
    'SYMINFO_FLG_DIRECT'   : 0x0001,
    'SYMINFO_FLG_PASSTHRU' : 0x0002,
    'SYMINFO_FLG_COPY'     : 0x0004,
    'SYMINFO_FLG_LAZYLOAD' : 0x0008,
    }
mirrorDict(syminfo_flags)

syminfo_version = {
    'SYMINFO_NONE'          : 0,
    'SYMINFO_CURRENT'       : 1,
    'SYMINFO_NUM'           : 2,
    }
mirrorDict(syminfo_version)


class SymbolTableEntry( Header ):
    descriptions_32 = [ 'st_name', 'st_value', 'st_size', 'st_info',
                        'st_other', 'st_shndx' ]

    descriptions_64 = [ 'st_name', 'st_info', 'st_other', 'st_shndx',
                        'st_value', 'st_size' ]

    format_32 = [ 'i', 'I', 'i', 'B', 'B', 'H' ]
    format_64 = [ 'i', 'B', 'B', 'H', 'Q', 'q' ]

    cf_descriptions = [ 'st_type', 'st_bind', 'st_visibility' ]

    cf_format = [ 'i', 'i', 'i' ]

    hr_values = {
        'st_type'       : [ VALUE_FIXED, symtab_type ],
        'st_bind'       : [ VALUE_FIXED, symtab_bind ],
        'st_visibility' : [ VALUE_FIXED, symtab_visibility ],
        }

    def __init__(self, prop=None, offset=None):
        self.name = 'null'

        Header.__init__(self, prop, offset)

    def get_st_type(self):
        return (self.st_info & 0xf)

    def get_st_bind(self):
        return (self.st_info >> 4)

    def get_st_visibility(self):
        return (self.st_other & 0x03)

    def set_st_bind(self, value):
        self._set_st_info(value, self.st_type)

    def set_st_type(self, value):
        self._set_st_info(self.st_bind, value)

    def set_st_info(self, st_bind, st_type):
        self.st_info = ((st_bind << 4) + (st_type & 0xf))

    def set_st_visibility(self, value):
        self.st_other = value & 0x03

class SymbolInfo( Header ):
    descriptions = [ 'si_boundto', 'si_flags' ]

    format = [ 'h', 'h' ]

    hr_values = {
        'si_boundto' : [ VALUE_FIXED, syminfo_boundto ],
        'si_flags'   : [ VALUE_BITWISE, syminfo_flags ],
        }

#######
# EOF #
#######

