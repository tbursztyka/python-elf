#!/usr/bin/python

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


dumpelf.py
----------

dumpelf.py is a simple Q&D example of what can be done with python-elf at this time. 
python-elf parses the binary file and provides useful functions/data to use.
Not that python-elf does NOT interpret the parsed informations. It's up so you to 
know how to use thoses. E.G. dumpelf.py knows which sections to use to disassemble. 
"""

from elf.elf_binary import Elf
from elf.printers import printHeader
from elf.section import shdr_type
from elf.elf_header import ehdr_machine
from elf.program import phdr_flags
from optparse import OptionParser, make_option
import sys

cannot_disassemble = False
try:
    from distorm import Decode, Decode32Bits, Decode64Bits
except:
    cannot_disassemble = true
    pass

if len(sys.argv) <= 1:
    print "dumpelf.py needs at least 1 argument."
    sys.exit(-1)

option_list = [
    make_option("-a", "--all", help="display everything (quite verbose), but do not disassemble.",
                action="store_true", dest="verbose"),
    make_option("-p", "--programs", help="display only Program headers.",
                action="store_true", dest="disp_programs"),
    make_option("-s", "--sections", help="display only Section headers.",
                action="store_true", dest="disp_sections"),
    make_option("-d", "--disassemble", help="disassemble relevant part. (needs distorm64 module)",
                action="store_true", dest="disassemble"),
    ]

parser = OptionParser(option_list=option_list)

parser.set_defaults(verbose=False, disp_programs=False, disp_sections=False, disassemble=False)
    
(options, args) = parser.parse_args()

verbose = options.verbose
disp_programs = options.disp_programs
disp_sections = options.disp_sections
disassemble = options.disassemble

if cannot_disassemble:
    print "distorm module is not present on your system."
    print "Disassemble capability is disabled."
    disassemble = False

binfile = sys.argv[len(sys.argv)-1]

try:
    bin = Elf(binfile)
except:
    print "Could not open %s" % binfile
    sys.exit(-1)

print 'ELF Header:'
print '\te_ident\n\t['
printHeader(bin.header.e_ident)
print '\t]'
printHeader(bin.header)
print '\n'

if not disp_programs and not disp_sections and not verbose and not disassemble:
    sys.exit(0)

if disp_programs or verbose:
    ndx = 0
    for prg in bin.programs:
        print 'Program Header #%d' % (ndx)
        printHeader(prg.header)
        ndx += 1

        print '\n'

if not disp_sections and not verbose and not disassemble:
    sys.exit(0)

ndx = 0
for sec in bin.sections:
    if disassemble:
        if sec.header.sh_type == shdr_type['SHT_PROGBITS'] and sec.header.sh_addr > 0x0:
            print 'Section Header #%d - %s' % (ndx, sec.name)
            mode = None

            if bin.header.e_machine == ehdr_machine['EM_X86_64']:
                mode = Decode64Bits
            elif bin.header.e_machine == ehdr_machine['EM_386']:
                mode = Decode32Bits

            if not mode:
                print "Cannot disassemble this binary file, its e_machine is not handled by distorm64."
                sys.exit(1)

            disas_list = Decode(sec.header.sh_addr, str(sec.data), mode)
        
            print 'Assembler:'
            for i in disas_list:
                print "\t0x%08x (%02x) %-20s %s" % (i[0],  i[1],  i[3],  i[2])
            print '\n'
        
        ndx += 1
        continue

    print 'Section Header #%d - %s' % (ndx, sec.name)
    ndx += 1
    printHeader(sec.header)

    if not verbose:
        print '\n'
        continue

    htype = sec.header.sh_type
    if htype == shdr_type['SHT_SYMTAB'] or htype == shdr_type['SHT_DYNSYM']:
        print '\n\tSymbol tables entries:'
        sym_ndx = 0
        for entry in sec.symtab:
            print '\t%d \"%s\"' % (sym_ndx, entry.name)
            printHeader(entry)
            print '\n'
            sym_ndx += 1
    
    elif htype == shdr_type['SHT_DYNAMIC']:
        print '\n\tDynamic tables entries:'
        dyn_ndx = 0
        for entry in sec.dynamic:
            print '\t%d' % (dyn_ndx)
            printHeader(entry)
            print '\n'
            dyn_ndx += 1
    
    elif htype == shdr_type['SHT_NOTE']:
        print '\n\tNote entrie(s):'
        note_ndx = 0
        for entry in sec.note:
            print '\t%d' % (note_ndx)
            printHeader(entry.header)
            print '\t-> name %s' % (entry.name)
            print '\t-> desc %s' % (entry.desc)
            print '\n'
            note_ndx += 1

    print '\n'

#######
# EOF #
#######
