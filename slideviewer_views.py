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
        namespace['title'] = title
        ids = list(handler.get_record_ids())
        print("ids = %s" % ids)
        if not ids:
            return {'images': {},
                    'title': title}
        print("handler.get_records() = %s" % handler.get_records())
        get_value = handler.get_record_value

        namespace['images'] = []
        for record in handler.get_records():
            #record = record[0]
            print("record.__class__ = %s" % record.__class__)
            print("record[0] = %s" % record[0])
            print("get_catalog_values = %s" % record.get_catalog_values())
            print('title = %s' % get_value(record, 'title'))
            #print('title = %s' % record.get_property('title'))
            namespace['images'].append({
                'description': handler.get_record_value(record, 'description'),
                'title': handler.get_record_value(record, 'title'),
                'img_link': handler.get_record_value(record, 'img_link'),
                'img_path': handler.get_record_value(record, 'img_path'),
                '__id__': handler.get_record_value(record, '__id__'),
                'target': handler.get_record_value(record, 'target')
                })
        
        print("namespace = %s" % namespace)

        return namespace
