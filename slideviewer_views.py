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

# Import from ikaaro

# Import from itws
from itws.sidebar.diaporama_views import Diaporama_View


class Slideviewer_View(Diaporama_View):

    template = '/ui/slideviewer/Slideviewer_View.xml'

    def get_namespace(self, resource, context):
        namespace = {}
        table = resource.get_resource(resource.order_path)
        handler = table.handler

        title = resource.get_title(fallback=False)
        ids = list(handler.get_record_ids())
        if not ids:
            return {'an_image': {},
                    'title': title}

        for record in handler.get_records():
            print("record = %s" % record)
            #an_image = {}
            #t get_value = handler.get_record_value
