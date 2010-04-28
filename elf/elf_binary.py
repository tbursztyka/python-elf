"""
  Copyright (C) 2008-2010  Tomasz Bursztyka

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

from mmap import mmap, PROT_READ, PROT_WRITE
from elf.core.property import Property
from elf.core.chunk import Chunk
from elf.elf_header import Eident, ElfHeader
from elf.section import SectionHeader, Section, shdr_type
from elf.symbol import symtab_type
from elf.program import ProgramHeader, Program
from elf.utils import getNameFromStrTab
from os.path import getsize

class Elf( Chunk ):
    " Elf class """
    def __init__(self, filename, access='r', load=True, backup=False):
        self.access = access
        
        if self.access == 'w':
            mode = PROT_READ | PROT_WRITE
        elif self.access == 'r':
            mode = PROT_READ
        else:
            mode = None
        
        size = getsize(filename)
        
        self.prop = Property(mode, backup, filename, size_src=size)
        
        self.header = None
        self.sections = []
        self.programs = []
        self.chunks = []
        
        Chunk.__init__(self, prop=self.prop, load=load, offset=0, size=size)

    def load(self, offset=None, filemap=None):
        self.loadBinary()
        self.loadHeader()
        self.loadPrograms()
        self.loadSections()
        self.loadSectionsNames()
        self.loadSymbolsNames()

    def loadBinary(self, filename=None):
        if filename == None:
            filename = self.prop.filename
        
        self.prop.file_src = file(filename, 'r+')
        self.prop.map_src = mmap(self.prop.file_src.fileno(), 
                                 0, prot=self.prop.mode)
    
    def loadHeader(self, hdr_off=None):
        if hdr_off == None:
            hdr_off = 0
        
        # eident can be loaded even if self.prop.arch is not the same 
        # as machine or file's value
        eident = Eident(prop=self.prop, offset=hdr_off)
        
        # Now we set the files's value 
        self.prop.arch = eident.getArch()
        self.prop.endian = eident.getEndian()
        
        self.header = ElfHeader(eident)

        if not self.header in self.chunks:
            self.chunks.append(self.header)
    
    def loadSections(self, shdr_off=None, num=None, ent_size=None):
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
            sec = Section(shdr)
            off += shdr.size
            self.sections.append(sec)

            if not sec in self.chunks:
                self.chunks.append(sec)
    
    def loadPrograms(self, phdr_off=None, num=None, ent_size=None):
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
            prg = Program(phdr)
            off += phdr.size
            self.programs.append(prg)

            if not prg in self.chunks:
                self.chunks.append(prg)
    
    def loadSectionsNames(self):
        # Load section name from shstrtab if possible
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
    
    def loadSymbolsNames(self):
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

    # NOT USABLE IN ITS CURRENT STATUS!
    def write(self):
        if self.prop.backup:
            f_dst = file(self.prop.filename+'_mod', 'w+')
            f_dst.write('\n'*PAGESIZE)
            f_dst.close()
            self.prop.file_dst = file(self.prop.filename+'_mod', 'r+')
            self.prop.map_dst = mmap(self.prop.file_dst.fileno(), 
                                     0, prot=self.prop.mode)
            
            self.prop.map_dst.resize(self.calculSize())
        
        # We first write the "contents"
        # and then: the headers
        ndx = 0
        for prg in self.programs:
            print 'ndx %d offset %d size %d' % (ndx, prg.header.p_offset, 
                                                prg.header.p_filesz)
            prg.write()
            ndx += 1
        
        ndx = 0
        for sec in self.sections:
            print 'ndx %d offset %d size %d' % (ndx, sec.header.sh_offset, 
                                                sec.header.sh_size)
            sec.write()
            ndx += 1
            
        off = self.header.e_phoff
        for prg in self.programs:
            prg.header.write(off)
            off += prg.header.size

        off = self.header.e_shoff
        for sec in self.sections:
            sec.header.write(off)
            off += sec.header.size

        self.header.write()
    
    def finalize(self):
        if self.prop.map_dst != None:
            self.prop.map_dst.close()
            self.prop.file_dst.close()
        
        self.prop.map_src.close()
        self.prop.file_src.close()
    
    def calculSize(self):
        # FIXME: re-compute the TRUE size
        return self.prop.size_src

#######
# EOF #
#######
