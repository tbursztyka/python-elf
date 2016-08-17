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

""" DynamicSectionEntry class """

from elf.core.property import VALUE_FIXED, VALUE_BITWISE
from elf.core.header import Header
from elf.utils import mirrorDict

dhdr_tag = {
    'DT_NULL'                       : 0,
    'DT_NEEDED'                     : 1,
    'DT_PLTRELSZ'                   : 2,
    'DT_PLTGOT'                     : 3,
    'DT_HASH'                       : 4,
    'DT_STRTAB'                     : 5,
    'DT_SYMTAB'                     : 6,
    'DT_RELA'                       : 7,
    'DT_RELASZ'                     : 8,
    'DT_RELAENT'                    : 9,
    'DT_STRSZ'                      : 10,
    'DT_SYMENT'                     : 11,
    'DT_INIT'                       : 12,
    'DT_FINI'                       : 13,
    'DT_SONAME'                     : 14,
    'DT_RPATH'                      : 15,
    'DT_SYMBOLIC'                   : 16,
    'DT_REL'                        : 17,
    'DT_RELSZ'                      : 18,
    'DT_RELENT'                     : 19,
    'DT_PLTREL'                     : 20,
    'DT_DEBUG'                      : 21,
    'DT_TEXTREL'                    : 22,
    'DT_JMPREL'                     : 23,
    'DT_BIND_NOW'                   : 24,
    'DT_INIT_ARRAY'                 : 25,
    'DT_FINI_ARRAY'                 : 26,
    'DT_INIT_ARRAYSZ'               : 27,
    'DT_FINI_ARRAYSZ'               : 28,
    'DT_RUNPATH'                    : 29,
    'DT_FLAGS'                      : 30,
    'DT_ENCODING'                   : 32,
    'DT_PREINIT_ARRAY'              : 32,
    'DT_PREINIT_ARRAYSZ'            : 33,
    'DT_NUM'                        : 34,
    'DT_LOOS'                       : 0x6000000d,
    'DT_HIOS'                       : 0x6ffff000,
    'DT_LOPROC'                     : 0x70000000,
    'DT_HIPROC'                     : 0x7fffffff,
    'DT_PROCNUM'                    : 0x32,
    }
dhdr_tag = mirrorDict(dhdr_tag)

dhdr_mips_tag = {
    'DT_MIPS_RLD_VERSION'           : 0x70000001,
    'DT_MIPS_TIME_STAMP'            : 0x70000002,
    'DT_MIPS_ICHECKSUM'             : 0x70000003,
    'DT_MIPS_IVERSION'              : 0x70000004,
    'DT_MIPS_FLAGS'                 : 0x70000005,
    'DT_MIPS_BASE_ADDRESS'          : 0x70000006,
    'DT_MIPS_MSYM'                  : 0x70000007,
    'DT_MIPS_CONFLICT'              : 0x70000008,
    'DT_MIPS_LIBLIST'               : 0x70000009,
    'DT_MIPS_LOCAL_GOTNO'           : 0x7000000a,
    'DT_MIPS_CONFLICTNO'            : 0x7000000b,
    'DT_MIPS_LIBLISTNO'             : 0x70000010,
    'DT_MIPS_SYMTABNO'              : 0x70000011,
    'DT_MIPS_UNREFEXTNO'            : 0x70000012,
    'DT_MIPS_GOTSYM'                : 0x70000013,
    'DT_MIPS_HIPAGENO'              : 0x70000014,
    'DT_MIPS_RLD_MAP'               : 0x70000016,
    'DT_MIPS_DELTA_CLASS'           : 0x70000017,
    'DT_MIPS_DELTA_CLASS_NO'        : 0x70000018,
    'DT_MIPS_DELTA_INSTANCE'        : 0x70000019,
    'DT_MIPS_DELTA_INSTANCE_NO'     : 0x7000001a,
    'DT_MIPS_DELTA_RELOC'           : 0x7000001b,
    'DT_MIPS_DELTA_RELOC_NO'        : 0x7000001c,
    'DT_MIPS_DELTA_SYM'             : 0x7000001d,
    'DT_MIPS_DELTA_SYM_NO'          : 0x7000001e,
    'DT_MIPS_DELTA_CLASSSYM'        : 0x70000020,
    'DT_MIPS_DELTA_CLASSSYM_NO'     : 0x70000021,
    'DT_MIPS_CXX_FLAGS'             : 0x70000022,
    'DT_MIPS_PIXIE_INIT'            : 0x70000023,
    'DT_MIPS_SYMBOL_LIB'            : 0x70000024,
    'DT_MIPS_LOCALPAGE_GOTIDX'      : 0x70000025,
    'DT_MIPS_LOCAL_GOTIDX'          : 0x70000026,
    'DT_MIPS_HIDDEN_GOTIDX'         : 0x70000027,
    'DT_MIPS_PROTECTED_GOTIDX'      : 0x70000028,
    'DT_MIPS_OPTIONS'               : 0x70000029,
    'DT_MIPS_INTERFACE'             : 0x7000002a,
    'DT_MIPS_DYNSTR_ALIGN'          : 0x7000002b,
    'DT_MIPS_INTERFACE_SIZE'        : 0x7000002c,
    'DT_MIPS_RLD_TEXT_RESOLVE_ADDR' : 0x7000002d,
    'DT_MIPS_PERF_SUFFIX'           : 0x7000002e,
    'DT_MIPS_COMPACT_SIZE'          : 0x7000002f,
    'DT_MIPS_GP_VALUE'              : 0x70000030,
    'DT_MIPS_AUX_DYNAMIC'           : 0x70000031,
    'DT_MIPS_NUM'                   : 0x32,
    }

dhdr_alpha_tag = {
    'DT_ALPHA_PLTRO'                : (0x70000000 + 0),
    'DT_ALPHA_NUM'                  : 1,
    }

dhdr_ppc_tag = {
    'DT_PPC_GOT'                    : (0x70000000 + 0),
    'DT_PPC_NUM'                    : 1,
    }

dhdr_ppc64_tag = {
    'DT_PPC64_GLINK'                : (0x70000000 + 0),
    'DT_PPC64_OPD'                  : (0x70000000 + 1),
    'DT_PPC64_OPDSZ'                : (0x70000000 + 2),
    'DT_PPC64_NUM'                  : 3,
    }

dhdr_ia64_tag = {
    'DT_IA_64_PLT_RESERVE'          : (0x70000000 + 0),
    'DT_IA_64_NUM'                  : 1,
    }

class DynamicSectionEntry( Header ):
    descriptions = [ 'd_tag', 'd_un' ]

    format_32 = [ 'I', 'I' ]
    format_64 = [ 'Q', 'Q' ]

    cf_descriptions = [ 'd_val', 'd_ptr' ]

    cf_format = [ 'I', 'I' ]

    hr_values = {
        'd_tag' : [ VALUE_FIXED, dhdr_tag ],
        }

    def get_d_val(self):
        return self.d_un

    def get_d_ptr(self):
        return self.d_un

    def set_d_val(self, value):
        self.d_un = value

    def set_d_ptr(self, value):
        self.d_un = value

#######
# EOF #
#######
