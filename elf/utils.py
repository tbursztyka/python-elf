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

# Utility functions

from elf.core.property import *
from elf.elf_header import *
from elf.section import *
from elf.symbol import *
from elf.program import *

def getNameFromStrTab(index, strtab):
    if index >= len(strtab):
        return 'null'

    name = ''
    l = strtab[index]
    while l != '\0':
        name += l
        index +=1
        l = strtab[index]

    if len(name) == 0:
        name = 'null'

    return name

def isChunkVoid(c):
    if c.offset_start == c.offset_end:
        return True
    
    return False

def isChunkVoidInside(c1, c2):
    if isChunkVoid(c1) and c1.offset_start == c2.offset_start:
        return True

    return False

# Is c1 before c2?
def isChunkBefore(c1, c2):
    if c1.offset_start < c2.offset_start and c1.offset_end <= c2.offset_start:
        return True

    return False

# Is c1 after c2?
def isChunkAfter(c1, c2):
    if c1.offset_start >= c2.offset_end and c1.offset_end > c2.offset_end:
        return True

    return False

# Is c1 partially before c2?
def isChunkPartlyBefore(c1, c2):
    if c1.offset_start < c2.offset_start and c1.offset_end < c2.offset_end:
        if c1.offset_end > c2.offset_start:
            return True

    return False

# Is c1 partially after c2?
def isChunkPartlyAfter(c1, c2):
    return isChunkPartlyBefore(c2, c1)

# Is c1 overlapping c2?
def isChunkOverlapping(c1, c2):
    if c1.offset_start == c2.offset_start and c1.offset_end == c2.offset_end:
        return True

    return False

# Is c1 in c2?
def isChunkInside(c1, c2):
    if isChunkOverlapping(c1, c2):
        return True

    if c1.offset_start >= c2.offset_start and c1.offset_end <= c2.offset_end:
        return True

    return False

def isChunkSuperior(c1, c2):
    if isChunkBefore(c1, c2):
        return True

    if isChunkPartlyBefore(c1, c2):
        return True

    if isChunkInside(c2, c1):
        return True

    if isChunkOverlapping(c1, c2):
        return True

    return False

def heapify(chunks, node, n):
    k = node
    if k == 0:
        j = 1
    else:
        j = 2*k

    while j <= n:
        if j < n and isChunkSuperior(chunks[j], chunks[j+1]):
            j += 1
            
        if isChunkSuperior(chunks[k], chunks[j]):
            xchg = chunks[k]
            chunks[k] = chunks[j]
            chunks[j] = xchg

            k = j
            j = 2 * k
        else:
            break

def sortChunks(chunks):
    length = len(chunks)
    for i in range(length-1, -1, -1):
        heapify(chunks, i, length-1)

    for i in range(length-1, 0, -1):
        xchg = chunks[0]
        chunks[0] = chunks[i]
        chunks[i] = xchg

        heapify(chunks, 0, i - 1)

def makeChunkTree(chunks):
    sortChunks(chunks)

    for i in range(len(chunks)-1, 0, -1):
        if isChunkPartlyAfter(chunks[i], chunks[i-1]):
            chunks[i].partly_after = chunks[i-1]
            chunks[i-1].partly_before = chunks[i]
            continue
        
        if isChunkOverlapping(chunks[i], chunks[i-1]):
            chunks[i].overlap = chunks[i-1]
            chunks[i-1].addinclude(chunks[i])
            continue

        #for j in range(i-1, 0, -1):
        if isChunkInside(chunks[i], chunks[i-1]):
            chunks[i-1].addinclude(chunks[i])

    for i in range(len(chunks)-1, 0, -1):
        for j in range(i-1, 0, -1):
            if isChunkInside(chunks[i], chunks[j]):
                if chunks[i].inside != None:
                    chunks[j].addinclude(chunks[i])

    tree = []
    for c in chunks:
        tree.append(c)

    for t in tree:
        if t.inside != None:
            chunks.remove(t)
