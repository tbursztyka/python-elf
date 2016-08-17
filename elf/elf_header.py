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

""" Eident and ElfHeader classes """

from elf.core.property import ARCH_32, ARCH_64, LITTLE_ENDIAN, BIG_ENDIAN, \
                                                VALUE_FIXED, VALUE_BITWISE
from elf.core.header import Header
from elf.utils import mirrorDict
from struct import calcsize

ehdr_magic = {
    'ELFMAG0' : 0x7f,
    'ELFMAG1' : 'E',
    'ELFMAG2' : 'L',
    'ELFMAG3' : 'F',
    }
ehdr_magic = mirrorDict(ehdr_magic)

ehdr_class = {
    'ELFCLASSNONE' : 0,
    'ELFCLASS32'   : 1,
    'ELFCLASS64'   : 2,
    'ELFCLASSNUM'  : 3,
    }
ehdr_class = mirrorDict(ehdr_class)

ehdr_encoding = {
    'ELFDATANONE' : 0,
    'ELFDATA2LSB' : 1,
    'ELFDATA2MSB' : 2,
    'ELFDATANUM'  : 3,
    }
ehdr_encoding = mirrorDict(ehdr_encoding)

ehdr_osabi = {
    'ELFOSABI_NONE'       : 0,
    'ELFOSABI_SYSV'       : 0,
    'ELFOSABI_HPUX'       : 1,
    'ELFOSABI_NETBSD'     : 2,
    'ELFOSABI_LINUX'      : 3,
    'ELFOSABI_SOLARIS'    : 6,
    'ELFOSABI_AIX'        : 7,
    'ELFOSABI_IRIX'       : 8,
    'ELFOSABI_FREEBSD'    : 9,
    'ELFOSABI_TRU64'      : 10,
    'ELFOSABI_MODESTO'    : 11,
    'ELFOSABI_OPENBSD'    : 12,
    'ELFOSABI_ARM'        : 97,
    'ELFOSABI_STANDALONE' : 255,
    }
ehdr_osabi = mirrorDict(ehdr_osabi)

ehdr_type = {
    'ET_NONE'   : 0,
    'ET_REL'    : 1,
    'ET_EXEC'   : 2,
    'ET_DYN'    : 3,
    'ET_CORE'   : 4,
    'ET_NUM'    : 5,
    'ET_LOOS'   : 0xfe00,
    'ET_HIOS'   : 0xfeff,
    'ET_LOPROC' : 0xff00,
    'ET_HIPROC' : 0xffff,
    }
ehdr_type = mirrorDict(ehdr_type)

ehdr_machine = {
    'EM_NONE'        : 0,
    'EM_M32'         : 1,
    'EM_SPARC'       : 2,
    'EM_386'         : 3,
    'EM_68K'         : 4,
    'EM_88K'         : 5,
    'EM_860'         : 7,
    'EM_MIPS'        : 8,
    'EM_S370'        : 9,
    'EM_MIPS_RS3_LE' : 10,
    'EM_PARISC'      : 15,
    'EM_VPP500'      : 17,
    'EM_SPARC32PLUS' : 18,
    'EM_960'         : 19,
    'EM_PPC'         : 20,
    'EM_PPC64'       : 21,
    'EM_S390'        : 22,
    'EM_V800'        : 36,
    'EM_FR20'        : 37,
    'EM_RH32'        : 38,
    'EM_RCE'         : 39,
    'EM_ARM'         : 40,
    'EM_FAKE_ALPHA'  : 41,
    'EM_SH'          : 42,
    'EM_SPARCV9'     : 43,
    'EM_TRICORE'     : 44,
    'EM_ARC'         : 45,
    'EM_H8_300'      : 46,
    'EM_H8_300H'     : 47,
    'EM_H8S'         : 48,
    'EM_H8_500'      : 49,
    'EM_IA_64'       : 50,
    'EM_MIPS_X'      : 51,
    'EM_COLDFIRE'    : 52,
    'EM_68HC12'      : 53,
    'EM_MMA'         : 54,
    'EM_PCP'         : 55,
    'EM_NCPU'        : 56,
    'EM_NDR1'        : 57,
    'EM_STARCORE'    : 58,
    'EM_ME16'        : 59,
    'EM_ST100'       : 60,
    'EM_TINYJ'       : 61,
    'EM_X86_64'      : 62,
    'EM_PDSP'        : 63,
    'EM_FX66'        : 66,
    'EM_ST9PLUS'     : 67,
    'EM_ST7'         : 68,
    'EM_68HC16'      : 69,
    'EM_68HC11'      : 70,
    'EM_68HC08'      : 71,
    'EM_68HC05'      : 72,
    'EM_SVX'         : 73,
    'EM_ST19'        : 74,
    'EM_VAX'         : 75,
    'EM_CRIS'        : 76,
    'EM_JAVELIN'     : 77,
    'EM_FIREPATH'    : 78,
    'EM_ZSP'         : 79,
    'EM_MMIX'        : 80,
    'EM_HUANY'       : 81,
    'EM_PRISM'       : 82,
    'EM_AVR'         : 83,
    'EM_FR30'        : 84,
    'EM_D10V'        : 85,
    'EM_D30V'        : 86,
    'EM_V850'        : 87,
    'EM_M32R'        : 88,
    'EM_MN10300'     : 89,
    'EM_MN10200'     : 90,
    'EM_PJ'          : 91,
    'EM_OPENRISC'    : 92,
    'EM_ARC_A5'      : 93,
    'EM_XTENSA'      : 94,
    'EM_NUM'         : 95,
    'EM_ALPHA'       : 0x9026,
    }
ehdr_machine = mirrorDict(ehdr_machine)

ehdr_version = {
    'EV_NONE'    : 0,
    'EV_CURRENT' : 1,
    'EV_NUM'     : 2,
    }
ehdr_version = mirrorDict(ehdr_version)

class Eident( Header ):
    descriptions = [ 'ei_magic', 'ei_class', 'ei_data', 'ei_version',
                     'ei_osabi', 'ei_abiversion', 'ei_pad', 'ei_nident' ]

    hr_values = {
        'ei_class'   : [ VALUE_FIXED, ehdr_class ],
        'ei_data'    : [ VALUE_FIXED, ehdr_encoding ],
        'ei_version' : [ VALUE_FIXED, ehdr_version ],
        'ei_osabi'   : [ VALUE_FIXED, ehdr_osabi ],
        }

    format = [ '4s', 'B', 'B', 'B', 'B', 'B', '6B', 'B' ]

    def getArch(self):
        if self.ei_class == ehdr_class['ELFCLASS32']:
            return ARCH_32
        elif self.ei_class == ehdr_class['ELFCLASS64']:
            return ARCH_64
        else:
            return self.ei_class

    def getEndian(self):
        if self.ei_data == ehdr_encoding['ELFDATA2LSB']:
            return LITTLE_ENDIAN
        elif self.ei_data == ehdr_encoding['ELFDATA2MSB']:
            return BIG_ENDIAN
        else:
            return ''

class ElfHeader( Header ):
    descriptions = [ 'e_type', 'e_machine', 'e_version', 'e_entry',
                     'e_phoff', 'e_shoff', 'e_flags', 'e_ehsize',
                     'e_phentsize', 'e_phnum', 'e_shentsize',
                     'e_shnum', 'e_shstrndx' ]

    hr_values = {
        'e_type'    : [ VALUE_FIXED, ehdr_type ],
        'e_machine' : [ VALUE_FIXED, ehdr_machine ],
        'e_version' : [ VALUE_FIXED, ehdr_version ],
        }

    format_32 = [ 'h', 'h', 'i', 'I', 'I', 'I', 'i',
                  'h', 'h', 'h', 'h', 'h', 'h' ]
    format_64 = [ 'h', 'h', 'i', 'Q', 'Q', 'Q', 'i',
                  'h', 'h', 'h', 'h', 'h', 'h' ]

    def __init__(self, e_ident, offset=None):
        self.e_ident = e_ident

        if offset == None:
            offset = calcsize(''.join(Eident.format))

        Header.__init__(self, e_ident.prop, offset)

    def chunks(self):
        return [self.e_ident, self]

#######
# EOF #
#######
