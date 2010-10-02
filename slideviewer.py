# -*- coding: UTF-8 -*-
# Copyright (C) 2010 Armel FORTUN <armel@maar.fr>>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from itools.gettext import MSG

from itws.sidebar.diaporama import Diaporama, DiaporamaTable


class Slideviewer(Diaporama):

    class_id = 'slideviewer'
    class_version = '20101002'
    class_title = MSG(u'Slideviewer')
    class_description = MSG(u'Slideviewer')


class SlideviewerTable(DiaporamaTable):
    
    class_id = 'slideviewer-table'


################################################################################
# Register
################################################################################
register_resource_class(Slideviewer)
register_resource_class(SlideviewerTable)
register_box(Slideviewer, allow_instanciation=True, is_content=True,
    is_side=False)