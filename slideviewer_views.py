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
from itools.handlers import checkid
from itools.datatypes import Integer, Unicode
from itools.gettext import MSG
from itools.core import merge_dicts

# Import from ikaaro
from ikaaro import messages
from ikaaro.forms import TextWidget
from ikaaro.resource_views import DBResource_Edit, EditLanguageMenu
from ikaaro.views import CompositeForm

# Import from itws
from itws.sidebar.diaporama_views import Diaporama_View
from itws.sidebar.diaporama_views import DiaporamaTable_View, DiaporamaTable_AddRecord
from itws.sidebar.diaporama_views import DiaporamaProxyBox_Edit


class Slideviewer_View(Diaporama_View):

    access = 'is_allowed_to_view'
    template = '/ui/slideviewer/Slideviewer_View.xml'
    styles = ['/ui/slideviewer/style.css']
    scripts = ['/ui/slideviewer/jquery.slideviewer.1.2.js',
        '/ui/slideviewer/jquery.easing.1.3.js']

    def get_namespace(self, resource, context):
        namespace = {}
        table = resource.get_resource(resource.order_path)
        handler = table.handler

        title = resource.get_title(fallback=False)
        namespace['title'] = title
        namespace['width'] = resource.get_property('width')
        namespace['height'] = resource.get_property('height')
        namespace['border'] = resource.get_property('border')
        namespace['square'] = resource.get_property('square')
        #print(resource.get_property('width'))

        ids = list(handler.get_record_ids())
        if not ids:
            return {'images': {},
                    'title': title}

        get_value = handler.get_record_value
        namespace['cssid'] = "%s-%s" % (checkid(title), id(self))
        namespace['images'] = []

        for record in handler.get_records():
            img_path = get_value(record, 'img_path')
            img_path_resource = table.get_resource(str(img_path), soft=True)
            if img_path_resource:
                img_path = context.get_link(img_path_resource)
            namespace['images'].append({
                'description': get_value(record, 'description'),
                'title': get_value(record, 'title'),
                'img_link': get_value(record, 'img_link'),
                # TODO: Get a ./ link instead of a /section/page/img/
                'img_path': img_path,
                '__id__': get_value(record, '__id__'),
                'target': get_value(record, 'target')
                })

        return namespace


class SlideviewerProxyBox_Edit(DBResource_Edit):

    schema = merge_dicts(DiaporamaProxyBox_Edit.schema,
        {"width": Integer,
        "height": Integer,
        "border": Unicode,
        "square": Unicode
        })

    widgets = DiaporamaProxyBox_Edit.widgets + [
        TextWidget('width', title=MSG(u'Width (px)'), size=3),
        TextWidget('height', title=MSG(u'Height (px)'), size=3),
        TextWidget('border', title=MSG(u'Border-color (#hexade)'), size=7),
        TextWidget('square', title=MSG(u'Square\'s color (#hexade)'), size=7)
        ]

    def get_value(self, resource, context, name, datatype):
        if name == 'title':
            language = resource.get_content_language(context)
            return resource.parent.get_property(name, language=language)
        if name == 'width':
            return resource.parent.get_property(name)
        if name == 'height':
            return resource.parent.get_property(name)
        if name == 'border':
            return resource.parent.get_property(name)
        if name == 'square':
            return resource.parent.get_property(name)
        return DBResource_Edit.get_value(self, resource, context, name,
                                         datatype)

    def action(self, resource, context, form):
        # Check edit conflict
        self.check_edit_conflict(resource, context, form)
        if context.edit_conflict:
            return

        # Save changes
        title = form['title']
        width = form['width']
        height = form['height']
        border = form['border']
        square = form['square']
        language = resource.get_content_language(context)
        # Set title to menufolder
        resource.parent.set_property('title', title, language=language)
        resource.parent.set_property('width', width)
        resource.parent.set_property('height', height)
        resource.parent.set_property('border', border)
        resource.parent.set_property('square', square)
        # Ok
        context.message = messages.MSG_CHANGES_SAVED


class SlideviewerTable_CompositeView(CompositeForm):

    access = 'is_allowed_to_edit'

    subviews = [ # diaporama folder edition view
                 SlideviewerProxyBox_Edit(title=MSG(u'Edit diaporama title and size')),
                 DiaporamaTable_AddRecord(title=MSG(u'Add new image')),
                 DiaporamaTable_View()
                 ]
    context_menus = [EditLanguageMenu()]

    def get_namespace(self, resource, context):
        # XXX Force GET to avoid problem in STLForm.get_namespace
        # side effect unknown
        real_method = context.method
        context.method = 'GET'
        views = [ view.GET(resource, context) for view in
        self.subviews ]
        context.method = real_method
        return {'views': views}
