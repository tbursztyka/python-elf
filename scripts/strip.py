#!/usr/bin/python

import sys
from elf.elf_binary import Elf

if len(sys.argv) <= 1 or len(sys.argv) > 2:
    print('You should provide only one binary file as input')
    sys.exit(1)

binfile = sys.argv[len(sys.argv)-1]

E = Elf(binfile, access = 'w')

for s in E.sections:
    s.remove()

E.header.e_shoff = 0
E.header.e_shentsize = 0
E.header.e_shnum = 0
E.header.e_shstrndx = 0

E.recompute()

E.write()

