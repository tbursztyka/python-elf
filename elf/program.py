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

""" ProgramHeader and Program classes """

from elf.core.property import VALUE_FIXED, VALUE_BITWISE
from elf.core.header import Header
from elf.core.page import Page

phdr_type = {
    'PT_NULL'              : 0,
    'PT_LOAD'              : 1,
    'PT_DYNAMIC'           : 2,
    'PT_INTERP'            : 3,
    'PT_NOTE'              : 4,
    'PT_SHLIB'             : 5,
    'PT_PHDR'              : 6,
    'PT_TLS'               : 7,
    'PT_NUM'               : 8,
    'PT_LOOS'              : 0x60000000,
    'PT_GNU_EH_FRAME'      : 0x6474e550,
    'PT_GNU_STACK'         : 0x6474e551,
    'PT_GNU_RELRO'         : 0x6474e552,
    'PT_PAX_FLAGS'         : 0x65041580,
    'PT_LOSUNW'            : 0x6ffffffa,
    'PT_SUNWBSS'           : 0x6ffffffa,
    'PT_SUNWSTACK'         : 0x6ffffffb,
    'PT_HISUNW'            : 0x6fffffff,
    'PT_HIOS'              : 0x6fffffff,
    'PT_LOPROC'            : 0x70000000,
    'PT_HIPROC'            : 0x7fffffff,
    'PT_MIPS_REGINFO'      : 0x70000000,
    'PT_MIPS_RTPROC'       : 0x70000001,
    'PT_MIPS_OPTIONS'      : 0x70000002,
    'PT_HP_TLS'            : (0x60000000 + 0x0),
    'PT_HP_CORE_NONE'      : (0x60000000 + 0x1),
    'PT_HP_CORE_VERSION'   : (0x60000000 + 0x2),
    'PT_HP_CORE_KERNEL'    : (0x60000000 + 0x3),
    'PT_HP_CORE_COMM'      : (0x60000000 + 0x4),
    'PT_HP_CORE_PROC'      : (0x60000000 + 0x5),
    'PT_HP_CORE_LOADABLE'  : (0x60000000 + 0x6),
    'PT_HP_CORE_STACK'     : (0x60000000 + 0x7),
    'PT_HP_CORE_SHM'       : (0x60000000 + 0x8),
    'PT_HP_CORE_MMF'       : (0x60000000 + 0x9),
    'PT_HP_PARALLEL'       : (0x60000000 + 0x10),
    'PT_HP_FASTBIND'       : (0x60000000 + 0x11),
    'PT_HP_OPT_ANNOT'      : (0x60000000 + 0x12),
    'PT_HP_HSL_ANNOT'      : (0x60000000 + 0x13),
    'PT_HP_STACK'          : (0x60000000 + 0x14),
    'PT_PARISC_ARCHEXT'    : 0x70000000,
    'PT_PARISC_UNWIND'     : 0x70000001,
    'PT_ARM_EXIDX'         : 0x70000001,
    'PT_IA_64_ARCHEXT'     : (0x70000000 + 0),
    'PT_IA_64_UNWIND'      : (0x70000000 + 1),
    'PT_IA_64_HP_OPT_ANOT' : (0x60000000 + 0x12),
    'PT_IA_64_HP_HSL_ANOT' : (0x60000000 + 0x13),
    'PT_IA_64_HP_STACK'    : (0x60000000 + 0x14),
    }
for key,value in phdr_type.items(): phdr_type[value] = key

phdr_flags = {
    'PF_X'              : (1 << 0),
    'PF_W'              : (1 << 1),
    'PF_R'              : (1 << 2),
    'PF_PAGEEXEC'       : (1 << 4),
    'PF_NOPAGEEXEC'     : (1 << 5),
    'PF_SEGMEXEC'       : (1 << 6),
    'PF_NOSEGMEXEC'     : (1 << 7),
    'PF_MPROTECT'       : (1 << 8),
    'PF_NOMPROTECT'     : (1 << 9),
    'PF_RANDEXEC'       : (1 << 10),
    'PF_NORANDEXEC'     : (1 << 11),
    'PF_EMUTRAMP'       : (1 << 12),
    'PF_NOEMUTRAMP'     : (1 << 13),
    'PF_RANDMMAP'       : (1 << 14),
    'PF_NORANDMMAP'     : (1 << 15),
    'PF_MASKOS'         : 0x0ff00000,
    'PF_MASKPROC'       : 0xf0000000,
    'PF_MIPS_LOCAL'     : 0x10000000,
    'PF_PARISC_SBP'     : 0x08000000,
    'PF_HP_PAGE_SIZE'   : 0x00100000,
    'PF_HP_FAR_SHARED'  : 0x00200000,
    'PF_HP_NEAR_SHARED' : 0x00400000,
    'PF_HP_CODE'        : 0x01000000,
    'PF_HP_MODIFY'      : 0x02000000,
    'PF_HP_LAZYSWAP'    : 0x04000000,
    'PF_HP_SBP'         : 0x08000000,
    'PF_ARM_SB'         : 0x10000000,
    'PF_IA_64_NORECOV'  : 0x80000000,
    }
for key,value in phdr_flags.items(): phdr_flags[value] = key

class ProgramHeader( Header ):
    descriptions_32 = [ 'p_type', 'p_offset', 'p_vaddr', 'p_paddr',
                        'p_filesz', 'p_memsz', 'p_flags', 'p_align' ]

    descriptions_64 = [ 'p_type', 'p_flags', 'p_offset', 'p_vaddr',
                     'p_paddr', 'p_filesz', 'p_memsz', 'p_align' ]

    hr_values = {
        'p_type'  : [ VALUE_FIXED, phdr_type ],
        'p_flags' : [ VALUE_BITWISE, phdr_flags ],
        }

    format_32 = [ 'i', 'I', 'I', 'I', 'i', 'i', 'i', 'I' ]
    format_64 = [ 'i', 'i', 'Q', 'Q', 'Q', 'q', 'q', 'Q' ]

class Program( Page ):
    def __init__(self, phdr):
        Page.__init__(self, phdr, phdr.p_offset, phdr.p_filesz)

#######
# EOF #
#######

