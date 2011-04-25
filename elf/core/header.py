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

""" Header class """

from elf.core.property import ARCH_32, ARCH_64
from elf.core.chunk import Chunk
from struct import pack, calcsize
try:
    from struct import unpack_from
except ImportError:
    from struct import unpack
    def unpack_from(fmt, buf, offset=0):
        size = calcsize(fmt)
        return unpack(fmt, buf[offset:offset + size])

class Header( Chunk ):
    """ Basic Header class: it targets all headers in ELF format """
    """ descriptions of bit fields """
    descriptions = None
    """ bit fields structure format """
    format = None
    """ compound field descriptions """
    cf_descriptions = None
    """ compound field format """
    cf_format = None
    """ Human Readable values for certain field """
    hr_values = None
    
    def __init__(self, prop=None, offset=None):
        """ Constructor """
        self.fields = None
        
        if not self.format:
            try:
                if prop.arch == ARCH_32:
                    self.format = self.format_32
                elif prop.arch == ARCH_64:
                    self.format = self.format_64
                else:
                    self.format = []
            except AttributeError:
                self.format = []
            
        if not self.descriptions:
            try:
                if prop.arch == ARCH_32:
                    self.descriptions = self.descriptions_32
                elif prop.arch == ARCH_64:
                    self.descriptions = self.descriptions_64
                else:
                    self.descriptions = []
            except AttributeError:
                self.descriptions = []

        if not self.cf_descriptions:
            try:
                if prop.arch == ARCH_32:
                    self.cf_descriptions = self.cf_descriptions_32
                elif prop.arch == ARCH_64:
                    self.cf_descriptions = self.cf_descriptions_64
            except AttributeError:
                pass

        if not self.cf_format:
            try:
                if prop.arch == ARCH_32:
                    self.cf_format = self.cf_format_32
                elif prop.arch == ARCH_64:
                    self.cf_format = self.cf_format_64
            except AttributeError:
                pass

        if not self.hr_values:
            try:
                if prop.arch == ARCH_32:
                    self.hr_values = self.hr_values_32
                elif prop.arch == ARCH_64:
                    self.hr_values = self.hr_values_64
                else:
                    self.hr_values = {}
            except AttributeError:
                self.hr_values = {}

        Chunk.__init__(self, prop, True, offset, 
                       calcsize(''.join(self.format)))
    
    def __getattr__(self, name):
        """ Attribute getter rewrite """
        if self.descriptions != None and name in self.descriptions:
            return self.fields[self.descriptions.index(name)]
        
        if self.cf_descriptions != None and name in self.cf_descriptions:
            return getattr(self, "get_"+name)()

        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError, name
    
    def __setattr__(self, name, value):
        """ Attribute setter rewrite """
        if self.descriptions != None and name in self.descriptions:
            self.modified = True
            self.fields[self.descriptions.index(name)] = value

        elif self.cf_descriptions != None and name in self.cf_descriptions:
            getattr(self,  "set_"+name)(value)

        else:
            self.__dict__[name] = value
    
    def load(self, offset=None, filemap=None):
        """ Loads header fields according to descriptions/format """
        Chunk.load(self, offset, filemap)
        
        self.fields = list(unpack_from(''.join([self.prop.endian]+self.format), 
                                       self.data))
        
        self.data = None

    def todata(self):
        """ Transcode fields into a byte string """
        data = ''  
        for idx in range(0, len(self.format)):
            data += pack(''.join([self.prop.endian]+self.format[idx]),
                         self.fields[idx])
        
        return data
    
    # UNUSABLE IN ITS CURRENT STATUS
    def write(self, offset=None, filemap=None):
        """ Writes header fields """
        self.data = self.toData()

        Chunk.write(self, offset, filemap)
    
    def verify(self):
        """ Basic sanity check """
        pass

#######
# EOF #
#######
