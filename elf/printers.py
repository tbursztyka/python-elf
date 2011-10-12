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

# Display functions

from elf.core.property import VALUE_FIXED, VALUE_BITWISE

def getElementAsString(hdr, fmt, elt, max_len):
    formats = {
        'B' : '%d',
        'H' : '%d',
        'h' : '%d',
        'I' : '0x%X',
        'i' : '%d',
        'Q' : '0x%X',
        'q' : '%d',
        's' : '%s',
        }

    value = hdr.__getattr__(elt)

    disp_str = '\t%s%s= %s' % (elt, ' '*(max_len-len(elt)+1), formats[fmt])
    disp_str = disp_str % (value)

    if hdr.hr_values.has_key(elt):
        k_elt = hdr.hr_values.get(elt)
    else:
        return disp_str

    if k_elt[0] == VALUE_FIXED:
        if k_elt[1].has_key(value):
            disp_str += '\t ( '+k_elt[1].get(value)+' )'
        else:
            disp_str += '\t ( UNKNOWN )'
    elif k_elt[0] == VALUE_BITWISE and value != 0:
        tested = 0
        disp_str += '\t ('
        for key in k_elt[1].iterkeys():
            if type(key) != str:
                continue

            val = k_elt[1].get(key)
            if (value & val) == val:
                disp_str += ' '+key+' '
                tested |= val

        if (tested ^ value) != 0:
            disp_str += ' UNKNOWN ('+str(tested ^ value)+') '
        disp_str += ')'
    else:
        disp_str += '\t ( UNDEF )'

    return disp_str


def printHeader(hdr):
    max_len = 0
    for elt in hdr.descriptions:
        if len(elt) > max_len:
            max_len = len(elt)

    for elt in hdr.descriptions:
        fmt = hdr.format[hdr.descriptions.index(elt)]
        fmt = fmt[len(fmt)-1]

        print getElementAsString(hdr, fmt, elt, max_len)

    if hdr.cf_descriptions:
        for elt in hdr.cf_descriptions:
            if len(elt) > max_len:
                max_len = len(elt)

        print '\n\tCompound fields:'
        for elt in hdr.cf_descriptions:
            fmt = hdr.cf_format[hdr.cf_descriptions.index(elt)]
            fmt = fmt[len(fmt)-1]

            print getElementAsString(hdr, fmt, elt, max_len)

#######
# EOF #
#######

