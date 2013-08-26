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

from mmap import mmap, ACCESS_READ, ACCESS_WRITE, PAGESIZE
from elf.core.property import Property
from elf.core.chunk import Chunk
from elf.elf_header import Eident, ElfHeader
from elf.section import SectionHeader, Section, shdr_type
from elf.symbol import symtab_type
from elf.program import ProgramHeader, Program
from elf.utils import getNameFromStrTab, compareChunks, orderChunks
from os.path import getsize

""" Elf class """

class Elf( Chunk ):
    """ Elf class """
    def __init__(self, filename, access='r', load=True, backup=False):
        """ Constructor """

        self.access = access

        if self.access == 'w':
            mode = ACCESS_WRITE
        elif self.access == 'r':
            mode = ACCESS_READ
        else:
            mode = None

        size = getsize(filename)

        self.prop = Property(mode, backup, filename, size_src=size)

        self.header = None
        self.sections = []
        self.programs = []

        Chunk.__init__(self, prop=self.prop, load=load, offset=0, size=size)

    def load(self, offset=None, filemap=None):
        """ Loads the ELF file and all specific parts """

        self.load_binary(offset, filemap)
        self.load_header()
        self.load_programs()
        self.load_sections()
        self.load_sections_names()
        self.load_symbols_names()

        # Now, creating the chunks hierarchy
        chunks = self.chunks()
        chunks_sorted = sorted(chunks, cmp=compareChunks)
        orderChunks(chunks_sorted)

    def load_binary(self, filename=None, offset=None, filemap=None):
        """ Loads the ELF file into a memory mapped file """

        if filename == None:
            filename = self.prop.filename

        self.prop.file_src = file(filename, 'r+')
        self.prop.map_src = mmap(self.prop.file_src.fileno(),
                                 0, access=self.prop.mode)

        Chunk.load(self, offset, filemap)

    def load_header(self, hdr_off=None):
        """ Loads ELF header """

        if hdr_off == None:
            hdr_off = 0

        # eident can be loaded even if self.prop.arch is not the same 
        # as machine or file's value
        e_ident = Eident(prop=self.prop, offset=hdr_off)

        # Now we set the files's value 
        self.prop.arch = e_ident.getArch()
        self.prop.endian = e_ident.getEndian()

        self.header = ElfHeader(e_ident)

    def load_sections(self, shdr_off=None, num=None, ent_size=None):
        """ Loads ELF sections """

        if shdr_off == None:
            shdr_off = self.header.e_shoff

        # offset should be in file
        if shdr_off >= self.prop.size_src:
            return

        if num == None:
            num = self.header.e_shnum

        if ent_size == None:
            ent_size = self.header.e_shentsize

        if shdr_off == 0 or num <= 0:
            return

        off = shdr_off
        for ndx in range(0, num):
            shdr = SectionHeader(self.prop, off)

            section = Section(shdr)
            self.sections.append(section)

            off += shdr.size

    def load_programs(self, phdr_off=None, num=None, ent_size=None):
        """ Loads ELF programs """

        if phdr_off == None:
            phdr_off = self.header.e_phoff

        if num == None:
            num = self.header.e_phnum

        if ent_size == None:
            ent_size = self.header.e_phentsize

        if phdr_off == 0 or num <= 0:
            return

        off = phdr_off
        for ndx in range(0, num):
            phdr = ProgramHeader(self.prop, off)

            program = Program(phdr)
            self.programs.append(program)

            off += phdr.size

    def load_sections_names(self):
        """ Loads sections names from shstrtab if possible """

        # index should exists in section table
        if self.header.e_shstrndx >= len(self.sections):
            return

        if self.header.e_shstrndx <= 0:
            return

        # Then related section should be strtab type of
        shstrtab = self.sections[self.header.e_shstrndx]
        if shstrtab.header.sh_type != shdr_type['SHT_STRTAB']:
            return

        # Then trying to set a name if possible
        for sec in self.sections:
            sec.name = getNameFromStrTab(sec.header.sh_name, shstrtab.strtab)

    def load_symbols_names(self):
        """ Loads symbols names from symtab if possible """

        # let's proceed through all sections to find symtab or dynsym sections
        for sec in self.sections:
            if sec.header.sh_type != shdr_type['SHT_SYMTAB']:
                if sec.header.sh_type != shdr_type['SHT_DYNSYM']:
                    continue

            # if so: sh_link should point on an existing section
            # which should own strtab type of
            if sec.header.sh_link >= len(self.sections):
                continue

            s_strtab = self.sections[sec.header.sh_link]
            if s_strtab.header.sh_type != shdr_type['SHT_STRTAB']:
                continue

            # for each symbol entry then: a name should be found in strtab
            # or then for symbol entry describing section it should be 
            # set to related section's name.
            for s_entry in sec.symtab:
                s_entry.name = getNameFromStrTab(s_entry.st_name,
                                                 s_strtab.strtab)
                if s_entry.name == 'null':
                    if s_entry.st_type == symtab_type['STT_SECTION']:
                        s_entry.name = self.sections[s_entry.st_shndx].name

    def insert(self, chunk):
        """ Insert a new chunk """

        chunks = self.chunks()

        chunk.inserted = True
        chunks.append(chunk)

        chunks_sorted = sorted(chunks, cmp=compareChunks)
        orderChunks(chunks_sorted)

    def recompute(self, branch = None, move = 0, end = 0):
        """ Recompute all chunck offsets and ordering after changes """

        if branch == None:
            branch = self
        else:
            if branch.suppressed == True and (
                    branch.inside == self or branch.inside.suppressed == True):
                if len(branch.includes) > 0:
                    move -= branch.includes[0].offset_start - branch.offset_start
                else:
                    move -= branch.size
            else:
                if branch.inside == self and branch.offset_start + move > end:
                    move = -(branch.offset_start - end)

                if isinstance(branch, Program) == False:
                    branch.offset_start += move
                    branch.offset_end += move
                else:
                    move = 0

        if branch.inserted == True:
            move += branch.size
            branch.inserted = False

        includes = []
        includes.extend(branch.includes)

        for sub_b in includes:
            (move, end, b_incs) = self.recompute(sub_b, move, end)

            if len(b_incs) > 0:
                idx = branch.includes.index(sub_b) + 1
                for b_inc in b_incs:
                    branch.includes.insert(idx, b_inc)
                    idx += 1

            if sub_b.suppressed == True:
                branch.del_include(sub_b)

        ret_includes = []
        if branch.suppressed == True:
            ret_includes = branch.includes
        elif branch != self and end < branch.offset_end:
            end = branch.offset_end
        elif branch == self:
            branch.offset_end = end

        return (move, end, ret_includes)

    def count(self):
        """ Returns the current count of chunks this file is made of """

        return self.counter.count

    def chunks(self):
        """ Returns the list of all chunks including the current Elf instance """

        chunk_lst = [self]

        chunk_lst.extend(self.header.chunks())

        for chunk in self.sections:
            chunk_lst.extend(chunk.chunks())

        for chunk in self.programs:
            chunk_lst.extend(chunk.chunks())

        return chunk_lst

    def write(self):
        """ Writes the current ELF map into a file """

        filename = self.prop.filename
        if self.prop.backup:
            filename = self.prop.filename+'_mod'

        f_dst = file(filename, 'wb')
        f_dst.write('\0'*PAGESIZE)
        f_dst.close()
        self.prop.file_dst = file(filename, 'r+')
        self.prop.map_dst = mmap(self.prop.file_dst.fileno(),
                                 0, access=self.prop.mode)
        self.prop.map_dst.resize(self.size)

        ret_size = Chunk.write(self, self.prop.map_dst)

        self.prop.map_dst.close()
        self.prop.map_dst = None
        self.prop.file_dst.close()
        self.prop.file_dst = None

        return ret_size

    def finalize(self):
        """ Close map before deleting the object """

        if self.prop.map_dst != None:
            self.prop.map_dst.close()
            self.prop.file_dst.close()

        self.prop.map_src.close()
        self.prop.file_src.close()

        Chunk.finalize(self)

#######
# EOF #
#######

