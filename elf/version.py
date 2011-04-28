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

""" VersionDefinition, AuxVersionDefinition, VersionDependency and
AuxVersionDependency classes """

from elf.core.header import Header

verdef_version = {
    'VER_DEF_NONE'    : 0,
    'VER_DEF_CURRENT' : 1,
    'VER_DEF_NUM'     : 2,
    }

verdef_flag = {
    'VER_FLG_BASE' : 0x1,
    'VER_FLG_WEAK' : 0x2,
    'VER_FLG_WEAK' : 0x2,
    }

verdep_version = {
    'VER_NEED_NONE'    : 0,
    'VER_NEED_CURRENT' : 1,
    'VER_NEED_NUM'     : 2,
    }

class VersionDefinition( Header ):
    descriptions = [ 'vd_version', 'vd_flags', 'vd_ndx', 'vd_cnt', 'vd_hash',
                     'vd_aux', 'vd_next' ]

    format = [ 'H', 'H', 'H', 'H', 'I', 'I', 'I' ]

class AuxVersionDefinition( Header ):
    descriptions = [ 'vda_name', 'vda_next' ]

    format = [ 'I', 'I' ]

class VersionDependency( Header ):
    descriptions = [ 'vn_version', 'vn_cnt', 'vn_file', 'vn_aux', 'vn_next' ]

    format = [ 'H', 'H', 'I', 'I', 'I' ]

class AuxVersionDependency( Header ):
    descriptions = [ 'vna_hash', 'vna_flags', 'vna_other', 'vna_name', 'vna_next' ]

    format = [ 'I', 'H', 'H', 'I', 'I' ]

#######
# EOF #
#######
