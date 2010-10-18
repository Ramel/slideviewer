# -*- coding: UTF-8 -*-
# Copyright (C) 2009-2010 Henry Obein <henry@itaapy.com>
# Copyright (C) 2010 Armel FORTUN <armel@maar.fr>
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

# Import from the Standard Library
from copy import deepcopy

# Import from itools
from itools.handlers import checkid
from itools.datatypes import Integer, Unicode, Boolean, XMLContent
from itools.gettext import MSG
from itools.core import merge_dicts
from itools.uri import get_reference
from itools.xml import XMLParser

# Import from ikaaro
from ikaaro import messages
from ikaaro.forms import TextWidget, BooleanRadio
from ikaaro.resource_views import DBResource_Edit, EditLanguageMenu
from ikaaro.views import CompositeForm
from ikaaro.table_views import Table_View, OrderedTable_View
from ikaaro.future.order import get_resource_preview

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
    uid = 0

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
        namespace['show_border'] = resource.get_property('show_border')

        ids = list(handler.get_record_ids())
        if not ids:
            return {'images': {},
                    'title': title}

        get_value = handler.get_record_value
        namespace['cssid'] = "%s-%s" % (checkid(title.replace('.','-')), self.uid)
        namespace['images'] = []

        for record in handler.get_records_in_order():
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
        self.uid += 1
        return namespace


class SlideviewerProxyBox_Edit(DBResource_Edit):

    schema = merge_dicts(DiaporamaProxyBox_Edit.schema,
        {"width": Integer,
        "height": Integer,
        "border": Unicode,
        "square": Unicode,
        "show_border": Boolean
        })

    widgets = DiaporamaProxyBox_Edit.widgets + [
        TextWidget('width', title=MSG(u'Width (px)'), size=4, maxlength=4),
        TextWidget('height', title=MSG(u'Height (px)'), size=4, maxlength=4),
        TextWidget('border', title=MSG(u'Image border-color (#FF0000)'),
            size=7, maxlength=7),
        TextWidget('square', title=MSG(u'Square\'s color (#FF0000)'),
            size=7, maxlength=7),
        BooleanRadio('show_border', title=MSG(u'Show images border-color'))
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
        if name == 'show_border':
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
        show_border = form['show_border']
        language = resource.get_content_language(context)
        # Set title to menufolder
        resource.parent.set_property('title', title, language=language)
        resource.parent.set_property('width', width)
        resource.parent.set_property('height', height)
        resource.parent.set_property('border', border)
        resource.parent.set_property('square', square)
        resource.parent.set_property('show_border', show_border)
        # Ok
        context.message = messages.MSG_CHANGES_SAVED


class SlideviewerTable_View(OrderedTable_View):

    def get_item_value(self, resource, context, item, column):
        if column == 'img_path':
            img_path = resource.handler.get_record_value(item, column)
            # NOTE img_path is unicode multiple -> multilingual
            image = resource.get_resource(str(img_path), soft=True)
            if not image:
                return None
            return get_resource_preview(image, 128, 64, 0, context)
        elif column == 'img_link':
            img_link = resource.handler.get_record_value(item, column)
            reference = get_reference(img_link)
            if reference.scheme:
                # Encode the reference '&' to avoid XMLError
                reference = XMLContent.encode(str(reference))
                return XMLParser('<a href="%s">%s</a>' % (reference, reference))
            # Split path/view
            reference_path = str(reference.path)
            view = None
            if reference_path.count(';'):
                reference_path, view = reference_path.split('/;' ,1)
            item_resource = resource.get_resource(reference_path, soft=True)
            if not item_resource:
                # Not found, just return the reference
                # Encode the reference '&' to avoid XMLError
                return XMLContent.encode(str(reference))
            # Build the new reference with the right path
            reference2 = deepcopy(reference)
            reference2.path = context.get_link(item_resource)
            if view:
                # Append the view
                reference2.path = '%s/;%s' % (reference2.path, view)
            # Encode the reference '&' to avoid XMLError
            # Reference : the reference used for the a content
            reference = XMLContent.encode(str(reference))
            # Reference2 : the reference used for href attribute
            reference2 = XMLContent.encode(str(reference2))
            return XMLParser('<a href="%s">%s</a>' % (reference2, reference))
        return Table_View.get_item_value(self, resource, context, item, column)


class SlideviewerTable_CompositeView(CompositeForm):

    access = 'is_allowed_to_edit'

    subviews = [ # diaporama folder edition view
                 SlideviewerProxyBox_Edit(title=MSG(u'Edit diaporama title and size')),
                 DiaporamaTable_AddRecord(title=MSG(u'Add new image')),
                 SlideviewerTable_View()
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
