# -*- coding: UTF-8 -*-
# Copyright (C) 2009-2010 Henry Obein <henry@itaapy.com>
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

# Import from itools
from itools.gettext import MSG
from itools.datatypes import Integer, Unicode, Boolean, String
from itools.core import merge_dicts

# Import from ikaaro
from ikaaro.registry import register_resource_class
from ikaaro.folder_views import GoToSpecificDocument
from ikaaro.table import OrderedTableFile
from ikaaro.future.menu import Target

# Import from itws
from itws.repository import register_box
from itws.sidebar.diaporama import Diaporama, DiaporamaTable, DiaporamaImagePathDatatype

from slideviewer_views import Slideviewer_View, SlideviewerTable_CompositeView


class SlideviewerTableFile(OrderedTableFile):

    record_properties = {
        'title': Unicode(multiple=True),
        'description': Unicode(multiple=True),
        'img_path': DiaporamaImagePathDatatype(multiple=True,
            mandatory=True), # multilingual
        'img_link': String,
        'target': Target(mandatory=True, default='_top')}


class SlideviewerTable(DiaporamaTable):

    class_id = 'slideviewer-table'
    class_handler = SlideviewerTableFile

    view = SlideviewerTable_CompositeView()


class Slideviewer(Diaporama):

    class_id = 'slideviewer'
    class_version = '20101003'
    class_title = MSG(u'Slideviewer')
    class_description = MSG(u'Slideviewer')

    # order
    order_class = SlideviewerTable

    view = Slideviewer_View()

    @classmethod
    def get_metadata_schema(cls):
        return merge_dicts(Diaporama.get_metadata_schema(),
            {'width': Integer(default=256),
            'height': Integer(default=256),
            'border': Unicode(default="#FF0000"),
            'square': Unicode(default="#FF0000"),
            'show_border': Boolean(default=True)
            })


################################################################################
# Register
################################################################################
register_resource_class(Slideviewer)
register_box(Slideviewer, allow_instanciation=True, is_content=True,
    is_side=False)
