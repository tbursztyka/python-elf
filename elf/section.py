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

""" SectionHeader and Section classes """

from elf.core.property import VALUE_FIXED, VALUE_BITWISE
from elf.core.header import Header
from elf.core.page import Page
from elf.symbol import SymbolTableEntry
from elf.relocation import RelocationEntry, RelocationAEntry
from elf.dynamic import DynamicSectionEntry
from elf.note import NoteHeader, Note
try:
    from struct import unpack_from
except ImportError:
    from struct import calcsize, unpack
    def unpack_from(fmt, buf, offset=0):
        size = calcsize(fmt)
        return unpack(fmt, buf[offset:offset + size])

shdr_index = {
    'SHN_UNDEF'              : 0,
    'SHN_LORESERVE'          : 0xff00,
    'SHN_LOPROC'             : 0xff00,
    'SHN_BEFORE'             : 0xff00,
    'SHN_AFTER'              : 0xff01,
    'SHN_HIPROC'             : 0xff1f,
    'SHN_LOOS'               : 0xff20,
    'SHN_HIOS'               : 0xff3f,
    'SHN_ABS'                : 0xfff1,
    'SHN_COMMON'             : 0xfff2,
    'SHN_XINDEX'             : 0xffff,
    'SHN_HIRESERVE'          : 0xffff,
    'SHN_MIPS_ACOMMON'       : 0xff00,
    'SHN_MIPS_TEXT'          : 0xff01,
    'SHN_MIPS_DATA'          : 0xff02,
    'SHN_MIPS_SCOMMON'       : 0xff03,
    'SHN_MIPS_SUNDEFINED'    : 0xff04,
    'SHN_PARISC_ANSI_COMMON' : 0xff00,
    'SHN_PARISC_HUGE_COMMON' : 0xff01,
    }
for key,value in shdr_index.items(): shdr_index[value] = key

shdr_type = {
    'SHT_NULL'               : 0,
    'SHT_PROGBITS'           : 1,
    'SHT_SYMTAB'             : 2,
    'SHT_STRTAB'             : 3,
    'SHT_RELA'               : 4,
    'SHT_HASH'               : 5,
    'SHT_DYNAMIC'            : 6,
    'SHT_NOTE'               : 7,
    'SHT_NOBITS'             : 8,
    'SHT_REL'                : 9,
    'SHT_SHLIB'              : 10,
    'SHT_DYNSYM'             : 11,
    'SHT_INIT_ARRAY'         : 14,
    'SHT_FINI_ARRAY'         : 15,
    'SHT_PREINIT_ARRAY'      : 16,
    'SHT_GROUP'              : 17,
    'SHT_SYMTAB_SHNDX'       : 18,
    'SHT_NUM'                : 19,
    'SHT_LOOS'               : 0x60000000,
    'SHT_GNU_HASH'           : 0x6ffffff6,
    'SHT_GNU_LIBLIST'        : 0x6ffffff7,
    'SHT_CHECKSUM'           : 0x6ffffff8,
    'SHT_LOSUNW'             : 0x6ffffffa,
    'SHT_SUNW_move'          : 0x6ffffffa,
    'SHT_SUNW_COMDAT'        : 0x6ffffffb,
    'SHT_SUNW_syminfo'       : 0x6ffffffc,
    'SHT_GNU_verdef'         : 0x6ffffffd,
    'SHT_GNU_verneed'        : 0x6ffffffe,
    'SHT_GNU_versym'         : 0x6fffffff,
    'SHT_HISUNW'             : 0x6fffffff,
    'SHT_HIOS'               : 0x6fffffff,
    'SHT_LOPROC'             : 0x70000000,
    'SHT_HIPROC'             : 0x7fffffff,
    'SHT_LOUSER'             : 0x80000000,
    'SHT_HIUSER'             : 0x8fffffff,
    }
for key,value in shdr_type.items(): shdr_type[value] = key

shdr_type_mips = {
    'SHT_MIPS_LIBLIST'       : 0x70000000,
    'SHT_MIPS_MSYM'          : 0x70000001,
    'SHT_MIPS_CONFLICT'      : 0x70000002,
    'SHT_MIPS_GPTAB'         : 0x70000003,
    'SHT_MIPS_UCODE'         : 0x70000004,
    'SHT_MIPS_DEBUG'         : 0x70000005,
    'SHT_MIPS_REGINFO'       : 0x70000006,
    'SHT_MIPS_PACKAGE'       : 0x70000007,
    'SHT_MIPS_PACKSYM'       : 0x70000008,
    'SHT_MIPS_RELD'          : 0x70000009,
    'SHT_MIPS_IFACE'         : 0x7000000b,
    'SHT_MIPS_CONTENT'       : 0x7000000c,
    'SHT_MIPS_OPTIONS'       : 0x7000000d,
    'SHT_MIPS_SHDR'          : 0x70000010,
    'SHT_MIPS_FDESC'         : 0x70000011,
    'SHT_MIPS_EXTSYM'        : 0x70000012,
    'SHT_MIPS_DENSE'         : 0x70000013,
    'SHT_MIPS_PDESC'         : 0x70000014,
    'SHT_MIPS_LOCSYM'        : 0x70000015,
    'SHT_MIPS_AUXSYM'        : 0x70000016,
    'SHT_MIPS_OPTSYM'        : 0x70000017,
    'SHT_MIPS_LOCSTR'        : 0x70000018,
    'SHT_MIPS_LINE'          : 0x70000019,
    'SHT_MIPS_RFDESC'        : 0x7000001a,
    'SHT_MIPS_DELTASYM'      : 0x7000001b,
    'SHT_MIPS_DELTAINST'     : 0x7000001c,
    'SHT_MIPS_DELTACLASS'    : 0x7000001d,
    'SHT_MIPS_DWARF'         : 0x7000001e,
    'SHT_MIPS_DELTADECL'     : 0x7000001f,
    'SHT_MIPS_SYMBOL_LIB'    : 0x70000020,
    'SHT_MIPS_EVENTS'        : 0x70000021,
    'SHT_MIPS_TRANSLATE'     : 0x70000022,
    'SHT_MIPS_PIXIE'         : 0x70000023,
    'SHT_MIPS_XLATE'         : 0x70000024,
    'SHT_MIPS_XLATE_DEBUG'   : 0x70000025,
    'SHT_MIPS_WHIRL'         : 0x70000026,
    'SHT_MIPS_EH_REGION'     : 0x70000027,
    'SHT_MIPS_XLATE_OLD'     : 0x70000028,
    'SHT_MIPS_PDR_EXCEPTION' : 0x70000029,
    }
shdr_type_parisc = {
    'SHT_PARISC_EXT'         : 0x70000000,
    'SHT_PARISC_UNWIND'      : 0x70000001,
    'SHT_PARISC_DOC'         : 0x70000002,
    }
shdr_type_alpha = {
    'SHT_ALPHA_DEBUG'        : 0x70000001,
    'SHT_ALPHA_REGINFO'      : 0x70000002,
    }
shdr_type_ia64 = {
    'SHT_IA_64_EXT'          : (0x70000000 + 0),
    'SHT_IA_64_UNWIND'       : (0x70000000 + 1),
    }

shdr_flags = {
    'SHF_WRITE'            : (1 << 0),
    'SHF_ALLOC'            : (1 << 1),
    'SHF_EXECINSTR'        : (1 << 2),
    'SHF_MERGE'            : (1 << 4),
    'SHF_STRINGS'          : (1 << 5),
    'SHF_INFO_LINK'        : (1 << 6),
    'SHF_LINK_ORDER'       : (1 << 7),
    'SHF_OS_NONCONFORMING' : (1 << 8),
    'SHF_GROUP'            : (1 << 9),
    'SHF_TLS'              : (1 << 10),
    'SHF_MASKOS'           : 0x0ff00000,
    'SHF_MASKPROC'         : 0xf0000000,
    'SHF_ORDERED'          : (1 << 30),
    'SHF_EXCLUDE'          : (1 << 31),
    }
for key,value in shdr_flags.items(): shdr_flags[value] = key

shdr_flags_mips = {
    'SHF_MIPS_GPREL'       : 0x10000000,
    'SHF_MIPS_MERGE'       : 0x20000000,
    'SHF_MIPS_ADDR'        : 0x40000000,
    'SHF_MIPS_STRINGS'     : 0x80000000,
    'SHF_MIPS_NOSTRIP'     : 0x08000000,
    'SHF_MIPS_LOCAL'       : 0x04000000,
    'SHF_MIPS_NAMES'       : 0x02000000,
    'SHF_MIPS_NODUPE'      : 0x01000000,
    }
shdr_flags_parisc = {
    'SHF_PARISC_SHORT'     : 0x20000000,
    'SHF_PARISC_HUGE'      : 0x40000000,
    'SHF_PARISC_SBP'       : 0x80000000,
    }
shdr_flag_alpha = {
    'SHF_ALPHA_GPREL'      : 0x10000000,
    }
shdr_flags_arm = {
    'SHF_ARM_ENTRYSECT'    : 0x10000000,
    'SHF_ARM_COMDEF'       : 0x80000000,
    }
shdr_flags_ia64 = {
    'SHF_IA_64_SHORT'      : 0x10000000,
    'SHF_IA_64_NORECOV'    : 0x20000000,
    }

class SectionHeader( Header ):
    descriptions = [ 'sh_name', 'sh_type', 'sh_flags', 'sh_addr', 
                     'sh_offset', 'sh_size', 'sh_link', 'sh_info',
                     'sh_addralign', 'sh_entsize' ]

    format_32 = [ 'i', 'i', 'i', 'I', 'I', 'i', 'i', 'i', 'i', 'i' ]
    format_64 = [ 'i', 'i', 'q', 'Q', 'Q', 'q', 'i', 'i', 'q', 'q' ]

    hr_values = {
        'sh_type'  : [ VALUE_FIXED, shdr_type ],
        'sh_flags' : [ VALUE_BITWISE, shdr_flags ],
        }

class Section( Page ):
    def __init__(self, shdr):
        self.name = 'null'

        self.strtab = {}
        self.symtab = []
        self.relocs = []
        self.dynamic = []
        self.note = []

        Page.__init__(self, shdr, shdr.sh_offset, shdr.sh_size)

    def load(self, offset=None, filemap=None):
        # Call specific loading func, depending on sh_type
        if self.header.sh_type == shdr_type['SHT_SYMTAB']:
            self.loadSymTab()
        elif self.header.sh_type == shdr_type['SHT_DYNSYM']:
            self.loadSymTab()
        elif self.header.sh_type == shdr_type['SHT_STRTAB']:
             self.loadStrTab()
        elif self.header.sh_type == shdr_type['SHT_REL']:
            self.loadRelocs()
        elif self.header.sh_type == shdr_type['SHT_RELA']:
            self.loadRelocs(True)
        elif self.header.sh_type == shdr_type['SHT_DYNAMIC']:
            self.loadDynamic()
        elif self.header.sh_type == shdr_type['SHT_NOTE']:
            self.loadNote()
        else:
            Page.load(self)

    def loadSymTab(self):
        off = self.offset_start
        for ent_count in range(0, self.size/self.header.sh_entsize):
            symtab_entry = SymbolTableEntry(self.prop, off)
            
            self.symtab.append(symtab_entry)
            off += self.header.sh_entsize 

    def loadStrTab(self):
        if self.size <= 0:
            return

        format = self.prop.endian+('s'*self.size)

        Page.load(self)
        
        self.strtab = list(unpack_from(format, self.data))
        if self.strtab[len(self.strtab)-1] != '\0':
            self.strtab.append('\0')

    def loadRelocs(self, addends=False):
        off = self.offset_start
        
        for ent_count in range(0, self.size/self.header.sh_entsize):
            if addends:
                reloc = RelocationEntry(self.prop, off)
            else:
                reloc = RelocationAEntry(self.prop, off)

            self.relocs.append(reloc)
            off += self.header.sh_entsize

    def loadDynamic(self):
        off = self.offset_start
        for ent_count in range(0, self.size/self.header.sh_entsize):
            dynamic_entry = DynamicSectionEntry(self.prop, off)
            
            self.dynamic.append(dynamic_entry)
            off += self.header.sh_entsize 

    def loadNote(self):
        off = self.header.sh_offset
        size = self.header.sh_size
        while size > 0:
            n_hdr = NoteHeader(self.prop, off)
            note = Note(n_hdr)

            self.note.append(note)

            size = size - n_hdr.size - note.size

    def chunks(self):
        c_lst = Page.chunks(self)
        
        c_lst.extend(self.symtab)
        c_lst.extend(self.relocs)
        c_lst.extend(self.dynamic)
        
        for c in self.note:
            c_lst.extend(c.chunks())

        return c_lst

#######
# EOF #
#######
