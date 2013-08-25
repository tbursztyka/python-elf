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

# Utility functions

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

def compareChunks(x, y):
    if x.offset_start < y.offset_start:
        return -1
    elif x.offset_start == y.offset_start:
        if x.offset_end < y.offset_end:
            return 1
        elif x.offset_end > y.offset_end:
            return -1
    else:
        return 1

    return 0

def orderChunks(lst, n_p = 0, n_c = 1):
    if len(lst) <= n_c:
        return 0

    while(n_c > 0):
        p = lst[n_p]
        c = lst[n_c]
        if c.offset_start <= p.offset_end and c.offset_end <= p.offset_end:
            p.add_include(c)
            n_c = orderChunks(lst, n_c, n_c+1)
        else:
            break

    return n_c

#######
# EOF #
#######

